#!/usr/bin/python

import subprocess
import sys
import socketserver

import os
from dotenv import load_dotenv

load_dotenv()

# These variables are used as settings
PORT       = int(os.getenv('PORT')) 
IFACE      = os.getenv('IFACE')
IP_ADDRESS = os.getenv('IP_ADDRESS')
NETMASK    = os.getenv('NETMASK')

from src.server import CaptivePortal

def migration():
    print("init: migration database")

def start(CaptivePortal):
    print("Updating iptables")
    print(".. Allow TCP DNS")
    subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", "53", "-j" ,"ACCEPT"])
    print(".. Allow UDP DNS")
    subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "udp", "--dport", "53", "-j" ,"ACCEPT"])
    print("... Setting an IP ADDRESS")
    subprocess.call(["ip", "addr", "add", IP_ADDRESS+NETMASK, "dev", IFACE])
    print(".. Allow traffic to captive portal")
    subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", str(PORT),"-d", IP_ADDRESS, "-j" ,"ACCEPT"])
    print(".. Block all other traffic")
    subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-j" ,"DROP"])
    print("Starting web server")

    httpd = socketserver.TCPServer(((IP_ADDRESS, PORT)), CaptivePortal)

    print("Redirecting HTTP traffic to captive portal")
    subprocess.call(["iptables", "-t", "nat", "-A", "PREROUTING", "-i", IFACE, "-p", "tcp", "--dport", "80", "-j" ,"DNAT", "--to-destination", IP_ADDRESS+":"+str(PORT)])

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    
if __name__ == "__main__":
    file, script = sys.argv
    start(CaptivePortal) if script == 'start' else migration()