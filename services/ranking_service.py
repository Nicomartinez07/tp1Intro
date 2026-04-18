import repositories.ranking_repository as db
from utils.error_handlers import ValidationError

def obtener_ranking(limit=10, offset=0):
    if limit <= 0:
        raise ValidationError("El parámetro '_limit' debe ser mayor a 0.")
    if offset < 0:
        raise ValidationError("El parámetro '_offset' no puede ser negativo.")

    return db.obtener_ranking(limit, offset)