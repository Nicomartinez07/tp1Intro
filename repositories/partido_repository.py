import db

def execute_query(query, params=None, select=True):
    conn = None
    cur = None
    try:
        conn = db.get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(query, params)

        if select: 
            return cur.fetchall()
        
        conn.commit()
        if query.strip().upper().startswith("INSERT"):
            return cur.lastrowid
        else:
            return cur.rowcount
    except Exception as e:
        if conn: 
            conn.rollback() # si hay un error en un post o put hay que revertir los cambios hecho a la DB para evitar datos corruptos 
        raise e
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def obtener_partidos(equipo=None, fecha=None, fase=None):
    query = "SELECT * FROM partidos WHERE 1=1" # el where 1=1 es necesario para poder unir el resto de condiciones en caso de necesario 
    params = []

    if equipo:
        query += " AND (equipo_local LIKE %s OR equipo_visitante LIKE %s)"
        params.extend([equipo, equipo])
    if fecha:
        query += " AND fecha >= %s AND fecha < DATE_ADD(%s, INTERVAL 1 DAY)" # la fecha en la DB es fecha y hora, pero el parametro es solamente fecha entonces asi devuelve todos los partidos desde las 00:00 hasta 23:59 (el dia entero)
        params.extend([fecha, fecha])
    if fase:
        query += " AND fase = %s"
        params.append(fase)

    partidos = execute_query(query, tuple(params))
    return partidos

def crear_partido(equipo_local, equipo_visitante, fecha, fase):
    query = """
            INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase) 
            VALUES (%s, %s, %s, %s)
            """
    params = (equipo_local, equipo_visitante, fecha, fase)

    new_id = execute_query(query, params, select=False)

    # buscamos el partido recien creado para pasarlo a la respuesta del endpoint 
    query = "SELECT * FROM partidos WHERE id = %s"
    new_partido = execute_query(query, (new_id,), select=True)

    return new_partido

def eliminar_partido(id):
    query = "DELETE FROM partidos WHERE id = %s"
    filas_afectadas = execute_query(query, (id,), select=False)
    return filas_afectadas > 0

def actualizar_resultado_de_partido(id, goles_local, goles_visitante):

    query = """
        UPDATE resultados 
        SET goles_local = %s, 
            goles_visitante = %s 
        WHERE partido_id = %s
    """
    params = (goles_local, goles_visitante, id)

    filas_afectadas = execute_query(query, params, select=False)
    if filas_afectadas == 0:
        query = """
            INSERT INTO resultados (partido_id, goles_local, goles_visitante)
            VALUES (%s, %s, %s)
        """
        execute_query(query, (id, goles_local, goles_visitante), select=False)
    query = """
        SELECT goles_local, goles_visitante 
        FROM resultados 
        WHERE partido_id = %s
    """
    new_resultado = execute_query(query, (id,), select=True)

    return new_resultado