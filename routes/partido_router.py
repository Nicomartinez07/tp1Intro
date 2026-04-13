from flask import Flask, request, jsonify, Blueprint
import services.partido_service as logic

app = Flask(__name__)
partidos_bp = Blueprint("partidos", __name__, url_prefix="/partidos")


#Partidos  --------------------------------------------------------------

# Terminar de hacer - agregar limit y offset - fecha format 
@partidos_bp.route("/", methods=["GET"])
def obtener_partidos():
    try: 
        equipo = request.args.get("equipo")
        fecha = request.args.get("fecha")
        fase = request.args.get("fase")

        partidos = logic.obtener_partidos(equipo, fecha, fase)
        
        return jsonify(partidos), 200

    except ValueError as ve: # Errores en la validacion del service 
        return jsonify({
        "errors": [
            {
                "code": "BAD_REQUEST",
                "message": str(ve),
                "level": "error",
            }
        ]
    }), 400

    except Exception as e: # Errores internos 
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

    
#  Terminar de hacer 
@partidos_bp.route("/", methods=["POST"])
def crear_partido():
    try: 
        parametros = request.get_json()

        new_partido = logic.crear_partido(parametros)

        return jsonify({"message": "Partido creado exitosamente", "partido": new_partido}), 201 #Created

        #409
    
    except ValueError as ve:
        return jsonify({
        "errors": [
            {
                "code": "BAD_REQUEST",
                "message": str(ve),
                "level": "error",
            }
        ]
    }), 400

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


#  Terminar de hacer
@partidos_bp.route("/<int:id>", methods=["GET"])
def obtener_partido_por_id(id):
    try:
        conn = db.get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    SELECT * FROM partidos WHERE id = %s
                    JOIN resultados ON partidos.id = resultados.partido_id
                    """, (id,))  # la coma es para que python no lo tome id como tupla, sino como un unico valor 
        partidos = cur.fetchone()
        if not partidos:
            return jsonify({"error": "Partido no encontrado"}), 404 #Not Found
        return jsonify(partidos), 200 #OK

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

# Terminar de hacer
@partidos_bp.route("/<int:id>", methods=["PUT"])
def reemplazar_partido(id):
    try:
        datos = request.get_json()
    
        if not datos or 'equipo_local' not in datos or 'equipo_visitante' not in datos or 'fecha' not in datos or 'fase' not in datos:
            return jsonify({'error': 'Los campos "equipo_local", "equipo_visitante", "fecha" y "fase" son obligatorios'}), 400 #Bad Request 

        conn = db.get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    UPDATE partidos 
                    SET equipo_local= %s, 
                        equipo_visitante= %s, 
                        fecha= %s, 
                        fase= %s 
                    WHERE id= %s """, (datos['equipo_local'], datos['equipo_visitante'], datos['fecha'], datos['fase'], id))

        conn.commit()
        return jsonify({"message": "Partido reemplazado exitosamente"}), 204 #No Content
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

# SIN HACER
@partidos_bp.route("/<int:id>", methods=["PATCH"])
def actualizar_partido(id):
    pass

#terminar de hacer 
@partidos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_partido(id):
    try:
        conn = db.get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    DELETE FROM partidos WHERE id = %s
                    """, (id,))
        conn.commit()
        return jsonify({"message": "Partido eliminado exitosamente"}), 204 #No Content

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

# HECHO
@partidos_bp.route("/<int:id>/resultado}", methods=["PUT"])
def actualizar_resultado_de_partido(id):
    try:
        conn = db.get_connection()
        datos = request.get_json()
        if (not datos or 
            'local' not in datos or 
            'visitante' not in datos):
            return jsonify({
                    "errors": [
                        {
                        "code": "BAD_REQUEST",
                        "message": "Solicitud Incompleta.",
                        "level": "error",
                        "description": "Faltaron datos necesarios para actualizar el resultado del partido."
                        }
                    ]
        }), 400 

        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    UPDATE resultados 
                    SET local= %s, 
                        visitante= %s 
                    WHERE partido_id= %s 
                    JOIN partidos ON resultados.partido_id = partidos.id""", (datos['local'], datos['visitante'], id))

        conn.commit()
        return jsonify({"message": "Partido actualizado exitosamente"}), 204 #No Content
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

# SIN HACER
@partidos_bp.route("/<int:id>/prediccion}", methods=["POST"])
def realizar_prediccion(id):
    try:
        #201
        #400
        #404
        #409

        pass
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
