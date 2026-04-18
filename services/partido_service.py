from datetime import datetime
import repositories.partido_repository as db
from utils.error_handlers import NotFoundError, ValidationError

global partido_params
partido_params = ["equipo_local", "equipo_visitante", "fecha", "fase"]
resultado_params = ["local", "visitante"]

def __validar_fecha(fecha_str, incluye_hora=False):
    formato = '%Y-%m-%d %H:%M:%S' if incluye_hora else '%Y-%m-%d' # datetime or date dependiendo del la request 
    try:
        return datetime.strptime(fecha_str, formato)
    except (ValueError, TypeError):
        raise ValidationError(f"Fecha invalida")

def obtener_partidos(equipo=None, fecha=None, fase=None, limit=10, offset=0):
    if fecha:
        __validar_fecha(fecha)

    if limit < 0 or offset < 0:
        raise ValidationError("Los parametros '_limit' y '_offset' deben ser enteros no negativos.")
    
    return db.obtener_partidos(equipo, fecha, fase, limit, offset)


def crear_partido(parametros):
    for campo in partido_params:
        if (campo not in parametros) or (not parametros[campo]):
            raise ValidationError(f"El campo '{campo}' es requerido.")

    equipo_local = parametros["equipo_local"]
    equipo_visitante = parametros["equipo_visitante"]
    fecha = parametros["fecha"]
    fase = parametros["fase"]

    __validar_fecha(fecha, True)

    new_partido = db.crear_partido(equipo_local, equipo_visitante, fecha, fase)
    return new_partido  

def reemplazar_partido(id, parametros):
    for campo in partido_params:
        if (campo not in parametros) or (not parametros[campo]):
            raise ValidationError(f"El campo '{campo}' es requerido.")

    equipo_local = parametros["equipo_local"]
    equipo_visitante = parametros["equipo_visitante"]
    fecha = parametros["fecha"]
    fase = parametros["fase"]

    __validar_fecha(fecha, True)

    partido_existente = db.obtener_partido_por_id(id)
    if not partido_existente:
        raise NotFoundError(f"No se encontró el partido con ID {id} para reemplazar.")

    partido_actualizado = db.reemplazar_partido(id, equipo_local, equipo_visitante, fecha, fase)
    
    return partido_actualizado

def actualizar_partido(id, parametros):
    if not parametros:
        raise ValidationError("No se enviaron datos para actualizar.")

    campos_a_actualizar = {}
    for campo in partido_params:
        value = parametros.get(campo)

        if campo in parametros and value:
            campos_a_actualizar[campo] = parametros[campo]

    if not campos_a_actualizar:
        raise ValidationError("No se enviaron campos válidos para actualizar.")

    if "fecha" in campos_a_actualizar:
        __validar_fecha(campos_a_actualizar["fecha"], True)

    partido_existente = db.obtener_partido_por_id(id)
    if not partido_existente:
        raise NotFoundError(f"No se encontró el partido con ID {id} para actualizar.")

    partido_actualizado = db.actualizar_partido_parcial(id, campos_a_actualizar)
    
    return partido_actualizado

def obtener_partido_por_id(id):
    partido = db.obtener_partido_por_id(id)
    
    if not partido:
        raise NotFoundError("No se encontró el partido")
    
    respuesta_estilizada = {
        "id": partido.get("id"),
        "equipo_local": partido.get("equipo_local"),
        "equipo_visitante": partido.get("equipo_visitante"),
        "fecha": partido.get("fecha").strftime("%Y-%m-%d") if partido.get("fecha") else None,
        "fase": partido.get("fase"),
        "resultado": {
            "local": partido.get("goles_local"),
            "visitante": partido.get("goles_visitante")
        }
    }
    return respuesta_estilizada

def eliminar_partido(id: int):   

    if not db.eliminar_partido(id): # Devuelve false si no se elimino nada 
        raise NotFoundError("No se encontró el partido")
    
    return 
    
def actualizar_resultado_de_partido(id, parametros):
    for campo in resultado_params:
        if (campo not in parametros) or (parametros[campo] is None):
            raise ValidationError(f"El campo '{campo}' es requerido.")
        
    partido = db.obtener_partido_por_id(id)
    if not partido:
        raise NotFoundError("No se encontró el partido")

    goles_local = parametros.get("local")
    goles_visitante = parametros.get("visitante")

    db.actualizar_resultado_de_partido(id, goles_local, goles_visitante)
    return 