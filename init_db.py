import mysql.connector 

with open("schema.sql", "r") as f:
    sql = f.read()

conn = mysql.connector.connect(
    "host": "localhost",
    "user": "root",
    "password": "password"
)

cursor = conn.cursor()
for statement in sql.split(";"):
    if statement.strip():
        cursor.execute(statement)
        conn.commit()
    
cursor.close()
conn.close()