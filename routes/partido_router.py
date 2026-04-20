from flask import Flask, request, jsonify, Blueprint
import services.partido_service as logic
from utils.error_handlers import created_response, ValidationError, NotFoundError

app = Flask(__name__)
partidos_bp = Blueprint("partidos", __name__, url_prefix="/partidos")


# ─── GET /partidos ────────────────────────────────────────────────────────────
@partidos_bp.route("/", methods=["GET"])
def obtener_partidos():
    equipo = request.args.get("equipo")
    fecha = request.args.get("fecha")
    fase = request.args.get("fase")
    limit = request.args.get('_limit', default=10, type=int)
    offset = request.args.get('_offset', default=0, type=int)

    partidos, total = logic.obtener_partidos(equipo, fecha, fase, limit, offset)

    if not partidos:
        if equipo:
            raise NotFoundError(f"No se encontraron partidos con el equipo '{equipo}'.")
        return "", 204

    return jsonify({"partidos": partidos, "total": total}), 200


# ─── POST /partidos ───────────────────────────────────────────────────────────

@partidos_bp.route("/", methods=["POST"])
def crear_partido():
    parametros = request.get_json()

    new_partido = logic.crear_partido(parametros)
    return created_response({"message": "Partido creado exitosamente", "partido": new_partido}, f"/partidos/{new_partido['id']}")


# ─── GET /partidos/{id} ───────────────────────────────────────────────────────
@partidos_bp.route("/<int:id>", methods=["GET"])
def obtener_partido_por_id(id):
    partido = logic.obtener_partido_por_id(id)
    return jsonify(partido), 200


# ─── PUT /partidos/{id} ───────────────────────────────────────────────────────
@partidos_bp.route("/<int:id>", methods=["PUT"])
def reemplazar_partido(id):
    parametros = request.get_json()
    logic.reemplazar_partido(id, parametros)
    return "", 204


# ─── PATCH /partidos/{id} ─────────────────────────────────────────────────────
@partidos_bp.route("/<int:id>", methods=["PATCH"])
def actualizar_partido(id):
    parametros = request.get_json()
    logic.actualizar_partido(id, parametros)
    return "", 204

# ─── DELETE /partidos/{id} ────────────────────────────────────────────────────
@partidos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_partido(id: int):
    logic.eliminar_partido(id)

    return "", 204


# ─── PUT /partidos/{id}/resultado ─────────────────────────────────────────────
@partidos_bp.route("/<int:id>/resultado", methods=["PUT"])
def actualizar_resultado_de_partido(id):
    parametros = request.get_json()
    logic.actualizar_resultado_de_partido(id, parametros)
    return "", 204


# ─── POST /partidos/{id}/prediccion ───────────────────────────────────────────

@partidos_bp.route("/<int:id>/prediccion", methods=["POST"])
def realizar_prediccion(id):
    datos = request.get_json()
    resultado = logic.realizar_prediccion(id, datos)
    return jsonify(resultado), 201


# ─── Catch-all para IDs no numéricos ─────────────────────────────────────────

@partidos_bp.route("/<id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def partido_id_invalido(id):
    raise ValidationError("El ID debe ser un número entero positivo.")

@partidos_bp.route("/<id>/resultado", methods=["GET", "PUT", "PATCH", "DELETE"])
def partido_resultado_id_invalido(id):
    raise ValidationError("El ID debe ser un número entero positivo.")

@partidos_bp.route("/<id>/prediccion", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def partido_prediccion_id_invalido(id):
    raise ValidationError("El ID debe ser un número entero positivo.")
