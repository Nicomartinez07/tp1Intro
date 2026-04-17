from datetime import datetime
import repositories.partido_repository as db

global partido_params
partido_params = ["equipo_local", "equipo_visitante", "fecha", "fase"]
resultado_params = ["goles_local", "goles_visitante"]

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

def obtener_partido_por_id(id):
    row = db.obtener_partido_por_id(id)
    
    if not row:
        raise ValueError("No se encontró el partido")
    respuesta_estilizada = {
        "id": row.get("id"),
        "equipo_local": row.get("equipo_local"),
        "equipo_visitante": row.get("equipo_visitante"),
        "fecha": row.get("fecha").strftime("%Y-%m-%d") if row.get("fecha") else None,
        "fase": row.get("fase"),
        "resultado": {
            "local": row.get("goles_local"),
            "visitante": row.get("goles_visitante")
        }
    }
    return respuesta_estilizada

def eliminar_partido(id):   
    if not id:
        raise ValueError("El campo 'id' es requerido.")
    
    if not db.eliminar_partido(id):
        raise ValueError("No se encontró el partido")
    
    return True
    
def actualizar_resultado_de_partido(parametros):
    for campo in resultado_params:
        if (campo not in parametros) or (parametros[campo] is None):
            raise ValueError(f"El campo '{campo}' es requerido.")
        
    id = parametros.get("id")
    goles_local = parametros.get("goles_local")
    goles_visitante = parametros.get("goles_visitante")

    new_resultado = db.actualizar_resultado_de_partido(id, goles_local, goles_visitante)

    if new_resultado is None:
        raise ValueError("No se encontró el partido")  

    return new_resultado