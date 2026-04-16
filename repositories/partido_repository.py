import db

#                                                    valores default para paginacion
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
    new_partido = db.execute_query(query, (new_id,))

    return new_partido #[0]