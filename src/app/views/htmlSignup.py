#!/usr/bin/python3

import os
from dotenv import load_dotenv

from .cssStatic import css

load_dotenv()

# These variables are used as settings
PORT       = int(os.getenv('PORT')) 
IP_ADDRESS = os.getenv('IP_ADDRESS')
MSG        = ""

# The Register page

html_signup = '''
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Register</title>
            <!-- Latest compiled and minified CSS -->
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
            <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.1/css/all.css">
        </head>
        <style>
            {3}
        </style>
        <body>
            <div class="register">
                <h1>Register</h1>
                <div class="links">
                    <a href="http://{0}:{1}/signin">Signin</a>
                    <a class='active'>Signup</a>
                </div>
                <form method="POST" action="do_signup" autocomplete="off">
                    <label for="username">
                        <i class="fas fa-user"></i>
                    </label>
                    <input type="text" name="username" placeholder="Username" id="username" required>
                    <label for="password">
                        <i class="fas fa-lock"></i>
                    </label>
                    <input type="password" name="password" placeholder="Password" id="password" required>
                    <label for="email">
                        <i class="fas fa-envelope"></i>
                    </label>
                    <input type="email" name="email" placeholder="Email" id="email" required>
                    <div class="msg">{2}</div>
                    <input type="submit" value="Register">
                </form>
            </div>
        </body>
    </html>
    '''.format(IP_ADDRESS, PORT, MSG, css)

def getViewSignupEncode(msg = ""):
    global MSG
    MSG = msg
    return html_signup.encode()