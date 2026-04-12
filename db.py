import mysql.connector
import os

def get_connection(database_name="prode_mundial_2026"):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password", # Asegurate que sea tu password de MySQL
        database=database_name
    )

def get_server_connection():
    # Conexión al servidor sin base de datos específica (para el CREATE DATABASE)
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password"
    )