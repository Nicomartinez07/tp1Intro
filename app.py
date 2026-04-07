from flask import Flask, request, jsonify
import db

app = Flask(__name__)

@app.route("/partidos", methods=["GET"])
def obtener_partidos():
    try:
        equipos = request.args.get("equipos")
        fecha = request.args.get("fecha")
        fase = request.args.get("fase")
        
        partidos = db.obtener_partidos()
        return jsonify(partidos), 200

        #204
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
    
@app.route("/partidos", methods=["POST"])
def crear_partido():
    try: 
        datos = request.get_json() #Trae los datos

        if (not datos or 
            'equipo_local' not in datos or 
            'equipo_visitante' not in datos or 
            'fecha' not in datos or 
            'fase' not in datos):
            return jsonify({"error": "Datos incompletos"}), 400 #Bad Request, faltan datos necesarios para crear el partido
        
        partidos = db.crear_partido()
        return jsonify(partidos), 201 #Created

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

@app.route("/partidos/<int:id>", methods=["GET"])
def obtener_partido_por_id(id):
    try:
        #200
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

@app.route("/partidos/<int:id>", methods=["PUT"])
def reemplazar_partido(id):
    try:
        datos = request.get_json()
    
        if not datos or 'equipo_local' not in datos or 'equipo_visitante' not in datos or 'fecha' not in datos or 'fase' not in datos:
            return jsonify({'error': 'Los campos "equipo_local", "equipo_visitante", "fecha" y "fase" son obligatorios'}), 400 #Bad Request 

        partido_modificado = db.actualizar_partido()
        if partido_modificado:
            return jsonify(partido_modificado), 204 #No Content 
    
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

@app.route("/partidos/<int:id>", methods=["PATCH"])
def actualizar_partido(id):

@app.route("/partidos", methods=["DELETE"])
def eliminar_partido():
    try:
        #204
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

@app.route("/partidos/<int:id>/resultado}", methods=["PUT"])
def actualizar_resultado_de_partido(id):
    try:
        #204
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

@app.route("/partidos/<int:id>/prediccion}", methods=["POST"])
def realizar_prediccion(id):
    try:
        #201
        #400
        #404
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

#Usuarios

@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    try:
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

@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    try:
        #201
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

@app.route("/usuarios/<int:id>", methods=["GET"])
def obtener_usuario_por_id(id):
    try:
        #200
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

@app.route("/usuarios/<int:id>", methods=["PUT"])
def reemplazar_usuario(id):
    try:
        #204
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

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    try:
        #204
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

@app.route("/ranking", methods=["GET"])
def obtener_ranking():
     try:
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

if __name__ == "__main__":
    app.run(debug=True)

