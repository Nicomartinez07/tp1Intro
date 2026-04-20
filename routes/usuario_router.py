from flask import Flask, request, jsonify, Blueprint
import services.usuario_service as logic


app = Flask(__name__)
usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


#Usuarios  --------------------------------------------------------------

@usuarios_bp.route("/", methods=["GET"])
def obtener_usuarios():
 try:
    nombre = request.args.get("nombre")
    email = request.args.get("email")
    limit = request.args.get('_limit', default=10, type=int)
    offset = request.args.get('_offset', default=0, type=int)

    usuarios, total = logic.obtener_usuarios(nombre, email, limit, offset)
  

    return jsonify(usuarios), 200

 except Exception as e:
        return jsonify({
            "errors": [{
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Ocurrió un error interno al obtener los usuarios",
                "level": "error",
                "description": str(e)
            }]
        }), 500
       
@usuarios_bp.route("/", methods=["POST"])
def crear_usuario():
    parametros = request.get_json()

    new_usuario = logic.crear_usuario(parametros)

    return jsonify({"message": "Usuario creado exitosamente", "Usuario": new_usuario}), 201 #Created

@usuarios_bp.route("/<int:id>", methods=["GET"])
def obtener_usuario_por_id(id):
   usuario = logic.obtener_usuario_por_id(id)

   response = {
       "usuario": usuario,
    }
   return jsonify(response), 200


@usuarios_bp.route("/<int:id>", methods=["PUT"])
def reemplazar_usuario(id):
    parametros = request.get_json()

    usuario_actualizado = logic.reemplazar_usuario(id, parametros)

    return jsonify({
        "usuario": usuario_actualizado
    }), 200

@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_usuario(id: int):
    logic.eliminar_usuario(id)

    return "", 204


