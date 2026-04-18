import db

def obtener_ranking(limit: int, offset: int):
    # cantidad TOTAL de usuarios en el ranking (sin limit ni offset) para el HATEOAS
    count_query = """
        SELECT COUNT(DISTINCT p.usuario_id) as total
        FROM predicciones p
        INNER JOIN resultados r ON p.partido_id = r.partido_id
    """
    cantidad_usuarios = db.execute_query(count_query, un_solo_valor=True)
    total = cantidad_usuarios['total'] if cantidad_usuarios else 0

    # los puntos deberia ser un campo de usuarios que se va modificando con cada prediccion en vez de tener que calcularlo asi.
    query = """
        SELECT 
            p.usuario_id AS id_usuario,
            SUM(
                CASE 
                    WHEN p.prediccion_local = r.goles_local AND p.prediccion_visitante = r.goles_visitante THEN 3
                    WHEN SIGN(p.prediccion_local - p.prediccion_visitante) = SIGN(r.goles_local - r.goles_visitante) THEN 1
                    ELSE 0 
                END
            ) AS puntos
        FROM predicciones p
        INNER JOIN resultados r ON p.partido_id = r.partido_id
        GROUP BY p.usuario_id 
        ORDER BY puntos DESC, id_usuario ASC
        LIMIT %s OFFSET %s
    """
    
    ranking = db.execute_query(query, (limit, offset))

    return ranking, total