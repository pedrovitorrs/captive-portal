#!/usr/bin/python3

import http.server
import socketserver
import cgi

import os
from dotenv import load_dotenv

from src.app.views import htmlSignin, htmlRedirect, htmlSignup
from src.app.controllers import signinController

load_dotenv()

# These variables are used as settings
PORT       = int(os.getenv('PORT')) 
IFACE      = os.getenv('IFACE')
IP_ADDRESS = os.getenv('IP_ADDRESS')

'''
This it the http server used by the the captive portal
'''
class CaptivePortal(http.server.SimpleHTTPRequestHandler):    
    '''
    if the user requests the login page show it, else
    use the redirect page
    '''
    def do_GET(self):
        path = self.path
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if path == "/signin":
            self.wfile.write(htmlSignin.getViewSigninEncode())
        elif path == "/signup":
            self.wfile.write(htmlSignup.getViewSignupEncode())
        else:
            self.wfile.write(htmlRedirect.getViewRedirectEncode())
    '''
    this is called when the user submits the login form
    '''
    def do_POST(self):
        LIST_CONTENTS = []
        path = self.path
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={
                'REQUEST_METHOD':'POST',
                'CONTENT_TYPE':self.headers['Content-Type'],
                }
            )
        
        username = form.getvalue("username")
        password = form.getvalue("password")

        if path == "/do_signin":
            # dummy security check
            if signinController.validation(username, password, self.client_address[0], LIST_CONTENTS):
                self.wfile.write("You are now authorized. Navigate to any URL".encode())
            else:
                # show the login form
                self.wfile.write(htmlSignin.getViewSigninEncode(LIST_CONTENTS.pop()))