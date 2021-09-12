import subprocess

from .loggerHelper import write

def auth(remote_IP: str):
    write("[AUTHORIZE DEVICE] auth", "New authorization from" + remote_IP)

    # authorized user
    subprocess.call(["iptables","-t", "nat", "-I", "PREROUTING","1", "-s", remote_IP, "-j" ,"ACCEPT"])
    subprocess.call(["iptables", "-I", "FORWARD", "-s", remote_IP, "-j" ,"ACCEPT"])