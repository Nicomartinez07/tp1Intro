import repositories.usuario_repository as db
from utils.error_handlers import NotFoundError, ValidationError, DuplicateError
import mysql.connector

global usuario_params
usuario_params = ["nombre", "email"]

def obtener_usuarios(nombre=None, email=None, limit=10, offset=0):
    if limit < 1:
        raise ValidationError("El parámetro '_limit' debe ser mayor a 0.")
    if offset < 0:
        raise ValidationError("El parámetro '_offset' no puede ser negativo.")
    return db.obtener_usuarios(nombre, email, limit, offset)

def crear_usuario(parametros):
    for campo in usuario_params:
        if (campo not in parametros) or (not parametros[campo]):
            raise ValidationError(f"El campo '{campo}' es requerido.")

    nombre = parametros["nombre"]
    email = parametros["email"]

    if db.existe_email(email):
        raise DuplicateError("Ya existe un usuario con ese email.")

    try:
        return db.crear_usuario(nombre, email)
    except mysql.connector.errors.IntegrityError:
        raise DuplicateError("Ya existe un usuario con ese email.")

def obtener_usuario_por_id(id):
    usuario = db.obtener_usuario_por_id(id)
    
    if not usuario:
        raise NotFoundError("No se encontró el usuario")
    
    return usuario

def eliminar_usuario(id: int):   

    if not db.eliminar_usuario(id): # Devuelve false si no se elimino nada 
        raise NotFoundError("No se encontró el usuario")
        
    return 

def reemplazar_usuario(id, parametros):
    for campo in usuario_params:
        if (campo not in parametros) or (not parametros[campo]):
            raise ValidationError(f"El campo '{campo}' es requerido.")

    nombre = parametros["nombre"]
    email = parametros["email"]

    if db.existe_email(email, excluir_id=id):
        raise DuplicateError("Ya existe otro usuario con ese email.")

    try:
        db.reemplazar_usuario(id, nombre, email)
    except mysql.connector.errors.IntegrityError:
        raise DuplicateError("Ya existe otro usuario con ese email.")

