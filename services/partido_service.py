from datetime import datetime
import repositories.partido_repository as db

global partido_params
partido_params = ["equipo_local", "equipo_visitante", "fecha", "fase"]

def __validar_fecha(fecha_str, incluye_hora=False):
    formato = '%Y-%m-%d %H:%M:%S' if incluye_hora else '%Y-%m-%d' # datetime or date dependiendo del la request 
    try:
        return datetime.strptime(fecha_str, formato)
    except (ValueError, TypeError):
        raise ValueError(f"Fecha invalida")

def obtener_partidos(equipo=None, fecha=None, fase=None, limit=10, offset=0):
    if fecha:
        __validar_fecha(fecha)

    if limit < 0 or offset < 0:
        raise ValueError("Los parametros '_limit' y '_offset' deben ser enteros no negativos.")
    
    return db.obtener_partidos(equipo, fecha, fase, limit, offset)


def crear_partido(parametros):
    for campo in partido_params:
        if (campo not in parametros) or (not parametros[campo]):
            raise ValueError(f"El campo '{campo}' es requerido.")

    equipo_local = parametros["equipo_local"]
    equipo_visitante = parametros["equipo_visitante"]
    fecha = parametros["fecha"]
    fase = parametros["fase"]

    __validar_fecha(fecha, True)

    new_partido = db.crear_partido(equipo_local, equipo_visitante, fecha, fase)
    return new_partido  