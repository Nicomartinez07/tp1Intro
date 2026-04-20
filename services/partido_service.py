from datetime import datetime
import repositories.partido_repository as db
from utils.error_handlers import NotFoundError, ValidationError, DuplicateError
from services.usuario_service import obtener_usuario_por_id
import mysql.connector

global partido_params
partido_params = ["equipo_local", "equipo_visitante", "fecha", "fase"]
resultado_params = ["local", "visitante"]

FASES_VALIDAS = {"grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"}

def __validar_fecha(fecha_str, incluye_hora=False):
    if not isinstance(fecha_str, str):
        raise ValidationError("Fecha invalida")
    # Normalizar: quitar Z final y truncar milisegundos
    normalizada = fecha_str.rstrip('Z')
    if '.' in normalizada:
        normalizada = normalizada[:normalizada.index('.')]
    if incluye_hora:
        formatos = ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M', '%Y-%m-%d']
    else:
        formatos = ['%Y-%m-%d']
    for fmt in formatos:
        try:
            return datetime.strptime(normalizada, fmt)
        except ValueError:
            pass
    raise ValidationError("Fecha invalida")

def __validar_fase(fase):
    if fase not in FASES_VALIDAS:
        raise ValidationError(f"Fase invalida. Las fases válidas son: {', '.join(sorted(FASES_VALIDAS))}")

def obtener_partidos(equipo=None, fecha=None, fase=None, limit=10, offset=0):
    if limit < 1:
        raise ValidationError("El parámetro '_limit' debe ser mayor a 0.")
    if offset < 0:
        raise ValidationError("El parámetro '_offset' no puede ser negativo.")
    if fecha:
        __validar_fecha(fecha)
    if fase:
        __validar_fase(fase)

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
    __validar_fase(fase)

    if db.existe_partido(equipo_local, equipo_visitante, fecha, fase):
        raise DuplicateError("Ya existe un partido con los mismos datos.")

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
    __validar_fase(fase)

    db.reemplazar_partido(id, equipo_local, equipo_visitante, fecha, fase)

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
    if "fase" in campos_a_actualizar:
        __validar_fase(campos_a_actualizar["fase"])

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
        "fecha": partido.get("fecha").strftime("%Y-%m-%dT%H:%M:%S") if partido.get("fecha") else None,
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

def realizar_prediccion(id, datos):
    # 1. Validaciones
    
    campos_requeridos = ["id_usuario", "local", "visitante"]
    for campo in campos_requeridos:
        if campo not in datos:
            raise ValidationError(f"El campo '{campo}' es obligatorio.")

    # 2. Validar que el usuario exista
    usuario = obtener_usuario_por_id(datos["id_usuario"])
    if not usuario:
        raise NotFoundError(f"El usuario con ID {datos['id_usuario']} no existe.")

    # 3. Validar que el partido exista
    partido = obtener_partido_por_id(id)
    if not partido:
        raise NotFoundError(f"El partido con ID {id} no existe.")

    try:
        return db.realizar_prediccion(
            usuario_id=datos["id_usuario"],
            partido_id=id,
            prediccion_local=datos["local"],
            prediccion_visitante=datos["visitante"]
        )
    except mysql.connector.errors.IntegrityError:
        raise DuplicateError("El usuario ya tiene una predicción para este partido.")
