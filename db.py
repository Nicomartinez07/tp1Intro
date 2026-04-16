import mysql.connector
import os

def get_connection(database_name="prode_mundial_2026"):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="fiuba", # Asegurate que sea tu password de MySQL
        database=database_name
    )

def get_server_connection():
    # Conexión al servidor sin base de datos específica (para el CREATE DATABASE)
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="fiuba"
    )

def execute_query(query, params=None, modifica_db=False, un_solo_valor=False):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(query, params)

        if not modifica_db: 
            if un_solo_valor:
                return cur.fetchone()
            return cur.fetchall()
        
        # si la query es un insert o update hay que hacer commit() para que los cambios se guarden en la DB 
        conn.commit()
        return cur.lastrowid
    except Exception as e:
        if conn: 
            conn.rollback() # si hay un error en un post o put hay que revertir los cambios hecho a la DB para evitar datos corruptos 
        e.message = f"Error al ejecutar la query: {str(e)}. Query: {query}, Params: {params}"
        raise e
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()