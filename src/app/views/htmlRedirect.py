#!/usr/bin/python3

# This is the index of the captive portal
# it simply redirects the user to the to login page

import os
from dotenv import load_dotenv

load_dotenv()

# These variables are used as settings
PORT       = int(os.getenv('PORT')) 
IP_ADDRESS = os.getenv('IP_ADDRESS')

html_redirect = """
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=http://%s:%s/signin" />
    </head>
    <body>
        <b>Redirecting to login page</b>
    </body>
    </html>
    """%(IP_ADDRESS, PORT)

def getViewRedirectEncode():
    return html_redirect.encode()