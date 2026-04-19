import repositories.usuario_repository as db
from utils.error_handlers import NotFoundError, ValidationError

global usuario_params
usuario_params = ["nombre", "mail"] 

def obtener_usuarios(nombre=None, mail=None, limit=10, offset=0):
    if limit < 0 or offset < 0:
        raise ValidationError("Los parametros '_limit' y '_offset' deben ser enteros no negativos.")
    
    return db.obtener_usuarios(nombre, mail, limit, offset)