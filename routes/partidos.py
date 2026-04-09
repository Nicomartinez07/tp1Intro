from flask import Flask, request, jsonify, blueprints
import db

app = Flask(__name__)
partidos_bp = blueprints.Blueprint("partidos", __name__)


#Partidos  --------------------------------------------------------------

# Terminar de hacer - agregar limit y offset
@partidos_bp.route("/", methods=["GET"])
def obtener_partidos():
    try: 
        equipos = request.args.get("equipos")
        fecha = request.args.get("fecha")
        fase = request.args.get("fase")

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    SELECT * FROM partidos WHERE equipo_local LIKE %s OR equipo_visitante LIKE %s OR fecha = %s OR fase = %s
                    """, (equipos, equipos, fecha, fase))
        
        partidos = cur.fetchall()
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
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    
#  Terminar de hacer 
@partidos_bp.route("/", methods=["POST"])
def crear_partido():
    try: 
        datos = request.get_json()
        if (not datos or 
            'equipo_local' not in datos or 
            'equipo_visitante' not in datos or 
            'fecha' not in datos or 
            'fase' not in datos):
            return jsonify({"error": "Datos incompletos"}), 400 #Bad Request, faltan datos necesarios para crear el partido

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase) 
                    VALUES ('%s', '%s', '%s', '%s')
                    """, (datos['equipo_local'], datos['equipo_visitante'], datos['fecha'], datos['fase']))

        conn.commit()
        return jsonify({"message": "Partido creado exitosamente"}), 201 #Created

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

#  Terminar de hacer
@partidos_bp.route("/<int:id>", methods=["GET"])
def obtener_partido_por_id(id):
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    SELECT * FROM partidos WHERE id = %s
                    JOIN resultados ON partidos.id = resultados.partido_id
                    """, (id))
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

        conn = get_connection()
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

#terminar de hacer 
@partidos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_partido(id):
    try:
        conn = get_connection()
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

# SIN HACER
@partidos_bp.route("/<int:id>/resultado}", methods=["PUT"])
def actualizar_resultado_de_partido(id):
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
                    
                    """)
        conn.commit()
        return jsonify({"message": "Partido actualizado exitosamente"}), 204 #No Content
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

# SIN HACER
@partidos_bp.route("/<int:id>/prediccion}", methods=["POST"])
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
