#!/usr/bin/python3

import subprocess
import sys
import socketserver

import os
from dotenv import load_dotenv

from src.server import CaptivePortal
from src.database.ddl_sql import sql_create_tables
from src.helpers import loggerHelper

load_dotenv()

# These variables are used as settings
PORT       = int(os.getenv('PORT')) 
IFACE      = os.getenv('IFACE')
IP_ADDRESS = os.getenv('IP_ADDRESS')
NETMASK    = os.getenv('NETMASK')

# Boostrap logger helper
loggerHelper.setup()
loggerHelper.set_file_name()

def migration():
    loggerHelper.write("[INDEX] migration", "INIT: migration database")
    return sql_create_tables()

def start(CaptivePortal):
    loggerHelper.write("[INDEX] start", "Starting Server")
    loggerHelper.write("[INDEX] start", "Updating iptables")
    loggerHelper.write("[INDEX] start", "Allow TCP DNS")

    subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", "53", "-j" ,"ACCEPT"])
    
    loggerHelper.write("[INDEX] start", "Allow UDP DNS")
    
    subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "udp", "--dport", "53", "-j" ,"ACCEPT"])
    
    loggerHelper.write("[INDEX] start", "Setting an IP ADDRESS")
    
    subprocess.call(["ip", "addr", "add", IP_ADDRESS+NETMASK, "dev", IFACE])
    
    loggerHelper.write("[INDEX] start", "Allow traffic to captive portal")
    
    subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", str(PORT),"-d", IP_ADDRESS, "-j" ,"ACCEPT"])

    loggerHelper.write("[INDEX] start", "Block all other traffic")

    subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-j" ,"DROP"])

    loggerHelper.write("[INDEX] start", "Starting web server")

    httpd = socketserver.TCPServer(((IP_ADDRESS, PORT)), CaptivePortal)

    loggerHelper.write("[INDEX] start", "Redirecting HTTP traffic to captive portal")

    subprocess.call(["iptables", "-t", "nat", "-A", "PREROUTING", "-i", IFACE, "-p", "tcp", "--dport", "80", "-j" ,"DNAT", "--to-destination", IP_ADDRESS+":"+str(PORT)])

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    
if __name__ == "__main__":
    file, script = sys.argv
    start(CaptivePortal) if script == 'start' else migration()