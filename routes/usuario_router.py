from flask import Flask, request, jsonify, Blueprint
import services.usuario_service as logic
from utils.error_handlers import created_response, ValidationError

app = Flask(__name__)
usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


# ─── GET /usuarios ────────────────────────────────────────────────────────────

@usuarios_bp.route("/", methods=["GET"])
def obtener_usuarios():
    nombre = request.args.get("nombre")
    email = request.args.get("email")
    limit = request.args.get('_limit', default=10, type=int)
    offset = request.args.get('_offset', default=0, type=int)

    usuarios, total = logic.obtener_usuarios(nombre, email, limit, offset)

    if not usuarios:
        return "", 204

    return jsonify({"usuarios": usuarios, "total": total}), 200


# ─── POST /usuarios ───────────────────────────────────────────────────────────

@usuarios_bp.route("/", methods=["POST"])
def crear_usuario():
    parametros = request.get_json()
    new_usuario = logic.crear_usuario(parametros)
    return created_response({"message": "Usuario creado exitosamente", "usuario": new_usuario}, f"/usuarios/{new_usuario['id']}")


# ─── GET /usuarios/{id} ───────────────────────────────────────────────────────

@usuarios_bp.route("/<int:id>", methods=["GET"])
def obtener_usuario_por_id(id):
    usuario = logic.obtener_usuario_por_id(id)
    return jsonify(usuario), 200


# ─── PUT /usuarios/{id} ───────────────────────────────────────────────────────

@usuarios_bp.route("/<int:id>", methods=["PUT"])
def reemplazar_usuario(id):
    parametros = request.get_json()
    logic.reemplazar_usuario(id, parametros)
    return "", 204

# ─── DELETE /usuarios/{id} ────────────────────────────────────────────────────
@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_usuario(id: int):
    logic.eliminar_usuario(id)

    return "", 204


# ─── Catch-all para IDs no numéricos ─────────────────────────────────────────

@usuarios_bp.route("/<id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def usuario_id_invalido(id):
    raise ValidationError("El ID debe ser un número entero positivo.")
