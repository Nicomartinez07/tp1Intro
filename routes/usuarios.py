from flask import Flask, request, jsonify, blueprints
import db

app = Flask(__name__)
usuarios_bp = blueprints.Blueprint("usuarios", __name__)


#Usuarios  --------------------------------------------------------------

# terminar de hacer - agregar limit y offset como parametros de consulta y filtrar en base a eso
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    try:
        conn = db.get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    SELECT * FROM usuarios
                    """)
        
        usuarios = cur.fetchall()
        return jsonify(usuarios), 200
        #200
        #204
        #400
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
@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    try:
        datos = request.get_json()
        if (not datos or 
            'nombre' not in datos or 
            'email' not in datos):
            return jsonify({"error": "Datos incompletos"}), 400 #Bad Request, faltan datos necesarios para crear el partido

        conn = db.get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    INSERT INTO usuarios (nombre, email) 
                    VALUES ('%s', '%s')
                    """, (datos['nombre'], datos['email']))

        conn.commit()
        return jsonify({"message": "Usuario creado exitosamente"}), 201 #Created
        #400
        #409
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
@app.route("/usuarios/<int:id>", methods=["GET"])
def obtener_usuario_por_id(id):
    try:
        conn = db.get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    SELECT * FROM usuarios WHERE id = %s
                    """, (id))
        usuario = cur.fetchone()
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404 #Not Found
        return jsonify(usuario), 200 #OK
        #400
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

#terminar de hacer
@app.route("/usuarios/<int:id>", methods=["PUT"])
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
@app.route("/usuarios/<int:id>", methods=["DELETE"])
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
