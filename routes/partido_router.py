from flask import Flask, request, jsonify, Blueprint
import services.partido_service as logic

app = Flask(__name__)
partidos_bp = Blueprint("partidos", __name__, url_prefix="/partidos")


#Partidos  --------------------------------------------------------------


@partidos_bp.route("/", methods=["GET"])
def obtener_partidos():
    equipo = request.args.get("equipo")
    fecha = request.args.get("fecha")
    fase = request.args.get("fase")
    limit = request.args.get('_limit', default=10, type=int)
    offset = request.args.get('_offset', default=0, type=int)

    partidos, total = logic.obtener_partidos(equipo, fecha, fase, limit, offset)

    if not partidos:
        return jsonify({"message": "No se encontraron partidos con los criterios especificados."}), 204 # No Content

    response = {
        "partidos": partidos,
        "total": total
    }

    return jsonify(response), 200

    
@partidos_bp.route("/", methods=["POST"])
def crear_partido():
    parametros = request.get_json()

    new_partido = logic.crear_partido(parametros)

    return jsonify({"message": "Partido creado exitosamente", "partido": new_partido}), 201 #Created

    #409


# FALTA TERMINAR DE HACER 

@partidos_bp.route("/<int:id>", methods=["GET"])
def obtener_partido_por_id(id):
    partido = logic.obtener_partido_por_id(id)

    response = {
        "partido": partido,
    }
    
    return jsonify(response), 200


# Terminar de hacer
@partidos_bp.route("/<int:id>", methods=["PUT"])
def reemplazar_partido(id):
    parametros = request.get_json()

    partido_actualizado = logic.reemplazar_partido(id, parametros)

    return jsonify({
        "partido": partido_actualizado
    }), 200


@partidos_bp.route("/<int:id>", methods=["PATCH"])
def actualizar_partido(id):
    parametros = request.get_json()

    partido_actualizado = logic.actualizar_partido(id, parametros)

    return jsonify({
        "partido": partido_actualizado
    }), 200

#Hecho
@partidos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_partido(id: int):
    logic.eliminar_partido(id)

    return "", 204


    
# HECHO
@partidos_bp.route("/<int:id>/resultado", methods=["PUT"])
def actualizar_resultado_de_partido(id):
    parametros = request.get_json()

    logic.actualizar_resultado_de_partido(id, parametros)

    return "", 204
    
# Hecho

@partidos_bp.route("/<int:id>/prediccion", methods=["POST"])
def realizar_prediccion(id):
    datos = request.get_json()
    
    resultado = logic.realizar_prediccion(id, datos)
    return jsonify(resultado), 201