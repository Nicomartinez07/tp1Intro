import repositories.usuario_repository as db
from utils.error_handlers import NotFoundError, ValidationError

global usuario_params
usuario_params = ["nombre", "email"] 

def obtener_usuarios(nombre=None, email=None, limit=10, offset=0):
    if limit < 0 or offset < 0:
        raise ValidationError("Los parametros '_limit' y '_offset' deben ser enteros no negativos.")
    
    return db.obtener_usuarios(nombre, email, limit, offset)

def crear_usuario(parametros):
    for campo in usuario_params:
        if (campo not in parametros) or (not parametros[campo]):
            raise ValidationError(f"El campo '{campo}' es requerido.")

    nombre = parametros["nombre"]
    email = parametros["email"]
    
    new_usuario = db.crear_usuario(nombre, email)
    return new_usuario

def obtener_usuario_por_id(id):
    usuario = db.obtener_usuario_por_id(id)
    
    if not usuario:
        raise NotFoundError("No se encontró el usuario")
    
    return usuario

def eliminar_usuario(id: int):   

    if not db.eliminar_usuario(id): # Devuelve false si no se elimino nada 
        raise NotFoundError("No se encontró el usuario")
        
    return 