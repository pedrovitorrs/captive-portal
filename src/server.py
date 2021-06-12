#!/usr/bin/python

import subprocess
import http.server
import socketserver
import cgi

import os
from dotenv import load_dotenv

load_dotenv()

# These variables are used as settings
PORT       = int(os.getenv('PORT')) 
IFACE      = os.getenv('IFACE')
IP_ADDRESS = os.getenv('IP_ADDRESS')

'''
This it the http server used by the the captive portal
'''
class CaptivePortal(http.server.SimpleHTTPRequestHandler):
    #this is the index of the captive portal
    #it simply redirects the user to the to login page
    html_redirect = """
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=http://%s:%s/login" />
    </head>
    <body>
        <b>Redirecting to login page</b>
    </body>
    </html>
    """%(IP_ADDRESS, PORT)
    #the login page
    html_login = """
    <html>
    <body>
        <b>Login Form</b>
        <form method="POST" action="do_login">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """
    
    '''
    if the user requests the login page show it, else
    use the redirect page
    '''
    def do_GET(self):
        path = self.path
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if path == "/login":
            self.wfile.write(self.html_login.encode())
        else:
            self.wfile.write(self.html_redirect.encode())
    '''
    this is called when the user submits the login form
    '''
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        username = form.getvalue("username")
        password = form.getvalue("password")
        #dummy security check
        if username == 'nikos' and password == 'fotiou':
            #authorized user
            remote_IP = self.client_address[0]
            print('New authorization from ', remote_IP)
            print('Updating IP tables')
            subprocess.call(["iptables","-t", "nat", "-I", "PREROUTING","1", "-s", remote_IP, "-j" ,"ACCEPT"])
            subprocess.call(["iptables", "-I", "FORWARD", "-s", remote_IP, "-j" ,"ACCEPT"])
            self.wfile.write("You are now authorized. Navigate to any URL".encode())
        else:
            #show the login form
            self.wfile.write(self.html_login.encode())