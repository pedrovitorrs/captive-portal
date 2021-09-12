#!/usr/bin/python3

import os
import sys
import datetime

FILE_NAME = None
ROOT_DIR  = None
DIR_LOGS  = 'logs/'

'''
Get the root directory where the app is running
'''
def setup():
    global ROOT_DIR
    ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)
    # Do something slow

'''
Set the file name
'''
def set_file_name():
    global FILE_NAME
    FILE_NAME=datetime.datetime.now().strftime('%d/%m/%Y').replace('/', '')

'''
Write the excpect/info message in the log file
'''
def write(function_caller: str, message: str):
    global FILE_NAME
    if FILE_NAME:
        '''
        Create the file if dows not exists and open in append mode
        '''
        with open(ROOT_DIR+DIR_LOGS+FILE_NAME + '.log', 'a+') as f:
            f.write("{} -> {} {}\n".format(function_caller, datetime.datetime.now(), message))
    else:
        '''
        If the function that set the file name is not executed
        '''
        print("LOG: {}", message)