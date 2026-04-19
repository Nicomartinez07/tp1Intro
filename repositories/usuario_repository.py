import db

def obtener_usuarios(nombre=None, mail=None, limit=10, offset=0):
    
    query = "FROM usuarios WHERE 1=1" 
    params = []

   
    if nombre:
        query += " AND nombre LIKE %s"
        # Los % para que sea una búsqueda flexible. 
        # Si buscan "ale", va a encontrar a "Alejandro" y "Valeria"
        params.append(f"%{nombre}%") 
        
    if mail:
        query += " AND mail LIKE %s"
        params.append(f"%{mail}%")

    count_usuarios = db.execute_query("SELECT COUNT(*) as total " + query, tuple(params), un_solo_valor=True)
    total = count_usuarios['total'] if count_usuarios else 0

    lista_usuarios = db.execute_query("SELECT * " + query + " LIMIT %s OFFSET %s", tuple(params + [limit, offset]))
    
    return lista_usuarios, total