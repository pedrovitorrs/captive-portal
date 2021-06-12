import mysql.connector

import os
from dotenv import load_dotenv
from mysql.connector import errorcode

load_dotenv()

config = {
  'user': os.getenv('USER_DB'),
  'password': os.getenv('PASSWORD_DB'),
  'host': os.getenv('HOST_DB'),
  'database': os.getenv('DATABASE_DB'),
  'raise_on_warnings': True
}

def sql_open_connection():
  try: 
    conn = mysql.connector.connect(**config)
    return conn
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Infra Database: Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Infra Database: Database does not exist")
    else:
      print('Infra Database:' + err)
  else:
    sql_close_connection(conn)

def sql_close_connection(conn):
  conn.close()