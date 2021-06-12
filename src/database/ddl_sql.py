#!/usr/bin/python3
# DDL - DATA DEFINITION LANGUAGE 
# CREATE, ALTER, DROP, RENAME, TUNCATE COMMENT  

import mysql.connector
from mysql.connector import errorcode
from .infra_database import sql_open_connection, sql_close_connection

TABLES = {}
TABLES['clients'] = (
    "CREATE TABLE IF NOT EXISTS `user` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `name` VARCHAR(20) NOT NULL,"
    "  `email` VARCHAR(20) NOT NULL,"
    "  `password` VARCHAR(20) NOT NULL,"
    "  `created_at` DATE NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

def sql_create_table_user():
    connection = sql_open_connection()
    cursor = connection.cursor()
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("DDL SQL: Creating table {} -> ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Already exists.")
            else:
                print(err.msg)
        else:
            print("Created")

    cursor.close()
    sql_close_connection(connection)