import db

def obtener_partidos(equipo=None, fecha=None, fase=None, limit=10, offset=0):
    query = "FROM partidos WHERE 1=1" # el where 1=1 es necesario para poder unir el resto de condiciones en caso de necesario 
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

    count_partidos = db.execute_query("SELECT COUNT(*) as total " + query, tuple(params), un_solo_valor=True) # cada GET necesita hacer un count de TODOS los elementos por fuera del 'limit' para el HATEOS 
    total = count_partidos['total'] if count_partidos else 0

    lista_partidos = db.execute_query("SELECT * " + query + " LIMIT %s OFFSET %s", tuple(params + [limit, offset]))
    
    return lista_partidos, total 

def crear_partido(equipo_local, equipo_visitante, fecha, fase):
    query = """
            INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase) 
            VALUES (%s, %s, %s, %s)
            """
    params = (equipo_local, equipo_visitante, fecha, fase)

    new_id = db.execute_query(query, params, modifica_db=True)

    # buscamos el partido recien creado para pasarlo a la respuesta del endpoint 
    query = "SELECT * FROM partidos WHERE id = %s"
    new_partido = db.execute_query(query, (new_id,), un_solo_valor=True)

    return new_partido

def obtener_partido_por_id(id):
    query = """
        SELECT 
            p.id, 
            p.equipo_local, 
            p.equipo_visitante, 
            p.fecha, 
            p.fase,
            r.goles_local, 
            r.goles_visitante
        FROM partidos p
        LEFT JOIN resultados r ON p.id = r.partido_id 
        WHERE p.id = %s
    """ #left para traerme un partido sin resultado, porque sino no me traeria nada
    resultado = db.execute_query(query, (id,), un_solo_valor=True)
    return resultado

def eliminar_partido(id: int):
    query = "DELETE FROM partidos WHERE id = %s"
    filas_afectadas = db.execute_query(query, (id,), modifica_db=True)
    return filas_afectadas > 0

def actualizar_resultado_de_partido(id: int, goles_local: int, goles_visitante: int):
    # la query intenta hacer un insert primero, si el ID ya existe (osea que ya tiene un resultado), hace un UPDATE 
    query_upsert = """
        INSERT INTO resultados (partido_id, goles_local, goles_visitante)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            goles_local = VALUES(goles_local),
            goles_visitante = VALUES(goles_visitante)
    """
    db.execute_query(query_upsert, (id, goles_local, goles_visitante), modifica_db=True)

    return 

def reemplazar_partido(id, equipo_local, equipo_visitante, fecha, fase):
    query = """
        UPDATE partidos 
        SET equipo_local = %s, 
            equipo_visitante = %s, 
            fecha = %s, 
            fase = %s
        WHERE id = %s
    """
    params = (equipo_local, equipo_visitante, fecha, fase, id)
    
    db.execute_query(query, params, modifica_db=True)

    return obtener_partido_por_id(id)