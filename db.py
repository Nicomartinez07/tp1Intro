import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        "host": "localhost",
        "user": "root",
        "password": "password",
        "database": "prode_mundial_2026"
    ) 
    