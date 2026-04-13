import db

def execute_query(query, params=None):
    conn = None
    cur = None
    try:
        conn = db.get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(query, params)

        return cur.fetchall()
    except Exception as e:
        raise e
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def obtener_partidos(equipo=None, fecha=None, fase=None):
    print("PARAMETROS RECIBIDOS EN REPOSITORY: ", equipo, fecha, fase)
    query = "SELECT * FROM partidos WHERE 1=1" # el where 1=1 es necesario para poder unir el resto de condiciones en caso de necesario 
    params = []

    if equipo:
        query += " AND (equipo_local LIKE %s OR equipo_visitante LIKE %s)"
        params.extend([equipo, equipo])
    if fecha:
        query += " AND fecha = %s"
        params.append(fecha)
    if fase:
        query += " AND fase = %s"
        params.append(fase)

    partidos = execute_query(query, tuple(params))

    return partidos
