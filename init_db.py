import mysql.connector
import db 

with open("schema.sql", "r") as f:
    sql = f.read()

conn = db.get_connection()

cursor = conn.cursor()
for statement in sql.split(";"):
    if statement.strip():
        cursor.execute(statement)
        conn.commit()
    
cursor.close()
conn.close()    