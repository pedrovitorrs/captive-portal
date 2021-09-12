#!/usr/bin/python3

import os
from dotenv import load_dotenv

from .cssStatic import css

load_dotenv()

# These variables are used as settings
PORT       = int(os.getenv('PORT')) 
IP_ADDRESS = os.getenv('IP_ADDRESS')
MSG        = ""

# The login page

html_signin_old = """
    <html>
    <body>
        <b>Login Form</b>
        <form method="POST" action="do_signin">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """

html_signin = """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Login</title>
            <!-- Latest compiled and minified CSS -->
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
            <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.1/css/all.css">
        </head>
        <style>
            {3}
        </style>
        <body>
            <div class="login">
                <h1>Login</h1>
                <div class="links">
				    <a class='active'>Signin</a>
				    <a href="http://{0}:{1}/signup">Signup</a>
			    </div>
                <form method="POST" action="do_signin">
                    <label for="username">
                        <i class="fas fa-user"></i>
                    </label>
                    <input type="text" name="username" placeholder="Username" id="username" required>
                    <label for="password">
                        <i class="fas fa-lock"></i>
                    </label>
                    <input type="password" name="password" placeholder="Password" id="password" required>
                    <div class="msg">
                        <h3>{2}</h3>
                    </div>
                    <input type="submit" value="Login">
                </form>
            </div>
        </body>
    </html> 
    """.format(IP_ADDRESS, PORT, MSG, css)

def getViewSigninEncode(msg = ""):
    global MSG
    MSG = msg
    return html_signin.encode()