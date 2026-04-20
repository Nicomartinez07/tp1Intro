import db

def obtener_usuarios(nombre=None, email=None, limit=10, offset=0):
    
    query = "FROM usuarios WHERE 1=1" 
    params = []

   
    if nombre:
        query += " AND nombre LIKE %s"
        # Los % para que sea una búsqueda flexible. 
        # Si buscan "ale", va a encontrar a "Alejandro" y "Valeria"
        params.append(f"%{nombre}%") 
        
    if email:
        query += " AND email LIKE %s"
        params.append(f"%{email}%")

    count_usuarios = db.execute_query("SELECT COUNT(*) as total " + query, tuple(params), un_solo_valor=True)
    total = count_usuarios['total'] if count_usuarios else 0

    lista_usuarios = db.execute_query("SELECT * " + query + " LIMIT %s OFFSET %s", tuple(params + [limit, offset]))
    
    return lista_usuarios, total

def crear_usuario(nombre, email):
    query = """
            INSERT INTO usuarios (nombre, email) 
            VALUES (%s, %s)
            """
    params = (nombre, email)

    new_id = db.execute_query(query, params, modifica_db=True)

    # buscamos el usuario recien creado para pasarlo a la respuesta del endpoint 
    query = "SELECT * FROM usuarios WHERE id = %s"
    new_usuario = db.execute_query(query, (new_id,), un_solo_valor=True)

    return new_usuario

def obtener_usuario_por_id(id):
    query = """
        SELECT 
        u.id, 
        u.nombre, 
        u.email
    FROM usuarios u
    WHERE u.id = %s
    """
    resultado = db.execute_query(query, (id,), un_solo_valor=True)
    return resultado

def eliminar_usuario(id: int):
    query = "DELETE FROM usuarios WHERE id = %s"
    filas_afectadas = db.execute_query(query, (id,), modifica_db=True)
    return filas_afectadas > 0

def reemplazar_usuario(id, nombre, email):
    query = """
        UPDATE usuarios 
        SET nombre = %s, 
            email = %s
        WHERE id = %s
    """
    params = (nombre, email, id)

    db.execute_query(query, params, modifica_db=True)

    return obtener_usuario_por_id(id)
