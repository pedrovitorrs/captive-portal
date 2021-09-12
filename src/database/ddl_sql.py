#!/usr/bin/python3

# DDL - DATA DEFINITION LANGUAGE 
# CREATE, ALTER, DROP, RENAME, TUNCATE COMMENT  

import mysql.connector
from mysql.connector import errorcode

from .infra_database import sql_open_connection, sql_close_connection
from ..helpers import loggerHelper

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

def sql_create_tables():
    connection = sql_open_connection()
    cursor = connection.cursor()
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            loggerHelper.write("[DDL SQL] sql_create_tables", "Creating table {} -> ".format(table_name))
            cursor.execute(table_description)
            connection.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                loggerHelper.write("[DDL SQL] sql_create_tables", "Table Already exists.")
            else:
                loggerHelper.write("[DDL SQL] sql_create_tables", err.msg)
        else:
            loggerHelper.write("[DDL SQL] sql_create_tables", "Table created.")
    cursor.close()
    sql_close_connection(connection)