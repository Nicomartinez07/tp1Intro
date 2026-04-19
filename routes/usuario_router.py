from flask import Flask, request, jsonify, Blueprint
import services.usuario_service as logic


app = Flask(__name__)
usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


#Usuarios  --------------------------------------------------------------

# Hecho
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
       
# Hecho
@usuarios_bp.route("/", methods=["POST"])
def crear_usuario():
    parametros = request.get_json()

    new_usuario = logic.crear_usuario(parametros)

    return jsonify({"message": "Usuario creado exitosamente", "Usuario": new_usuario}), 201 #Created

# terminar de hacer
@usuarios_bp.route("/<int:id>", methods=["GET"])
def obtener_usuario_por_id(id):
   usuario = logic.obtener_usuario_por_id(id)

   response = {
       "usuario": usuario,
    }
   return jsonify(response), 200


#terminar de hacer
@usuarios_bp.route("/<int:id>", methods=["PUT"])
def reemplazar_usuario(id):
    try:
        datos = request.get_json()
        if not datos or 'nombre' not in datos or 'email' not in datos:
            return jsonify({'error': 'Los campos "nombre" y "email" son obligatorios'}), 400 #Bad Request 

        conn = db.get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    UPDATE usuarios 
                    SET nombre= %s, 
                        email= %s 
                    WHERE id= %s """, (datos['nombre'], datos['email'], id))

        conn.commit()
        return jsonify({"message": "Usuario reemplazado exitosamente"}), 204 #No Content
    except Exception as e:
        return jsonify({
        "errors": [
            {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Ocurrió un error interno",
                "level": "error",
                "description": str(e)
            }
        ]
    }), 500 #Internal Server Error
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# terminar de hacer
@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    try:
        conn = db.get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    DELETE FROM usuarios WHERE id = %s
                    """, (id,))
        conn.commit()
        return jsonify({"message": "Usuario eliminado exitosamente"}), 204 #No Content
        #400
        #404
    except Exception as e:
        return jsonify({
        "errors": [
            {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Ocurrió un error interno",
                "level": "error",
                "description": str(e)
            }
        ]
    }), 500 #Internal Server Error
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
