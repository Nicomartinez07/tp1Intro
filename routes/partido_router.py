from flask import Flask, request, jsonify, Blueprint
import services.partido_service as logic

app = Flask(__name__)
partidos_bp = Blueprint("partidos", __name__, url_prefix="/partidos")


#Partidos  --------------------------------------------------------------


@partidos_bp.route("/", methods=["GET"])
def obtener_partidos():
    try: 
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


# FALTA TERMINAR DE HACER 

@partidos_bp.route("/<int:id>", methods=["GET"])
def obtener_partido_por_id(id):
    try: 
        partido = logic.obtener_partido_por_id(id)
        response = {
            "partido": partido,
        }
        
        return jsonify(response), 200

    except ValueError as ve:
        mensaje = str(ve)

        if "No se encontró" in mensaje:
            code = "NOT_FOUND"
            status = 404
            descripcion = f"No se encontro el partido con el ID {id}."
        else:
            code = "BAD_REQUEST"
            status = 400
            descripcion = "Los parámetros de la solicitud son inválidos."

        return jsonify({
            "errors": [{
                "code": code,
                "message": mensaje,
                "description": descripcion,
                "level": "error"
            }]
        }), status
    
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

#Hecho
@partidos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_partido_endpoint(id):
    try: 
        logic.eliminar_partido(id)
        return "", 204

    except ValueError as ve:
        mensaje = str(ve)

        if "No se encontró" in mensaje:
            code = "NOT_FOUND"
            status = 404
            descripcion = f"No se encontro el partido con el ID {id}."
        else:
            code = "BAD_REQUEST"
            status = 400
            descripcion = "Los parámetros de la solicitud son inválidos."

        return jsonify({
            "errors": [{
                "code": code,
                "message": mensaje,
                "description": descripcion,
                "level": "error"
            }]
        }), status
    
    except Exception as e:
        # Log para el desarrollador en la consola
        print(f"Error inesperado: {e}") 
        return jsonify({
            "errors": [{
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Ocurrió un error interno al intentar eliminar",
                "level": "error"
            }]
        }), 500
# HECHO
@partidos_bp.route("/<int:id>/resultado", methods=["PUT"])
def actualizar_resultado_de_partido(id):
    try: 
        parametros = request.get_json()
        parametros["id"] = id

        logic.actualizar_resultado_de_partido(parametros)

        return "", 204

    except ValueError as ve:
        mensaje = str(ve)

        if "No se encontró" in mensaje:
            code = "NOT_FOUND"
            status = 404
            descripcion = f"No se encontro el partido con el ID {id}."
        else:
            code = "BAD_REQUEST"
            status = 400
            descripcion = "Los parámetros de la solicitud son inválidos."

        return jsonify({
            "errors": [{
                "code": code,
                "message": mensaje,
                "description": descripcion,
                "level": "error"
            }]
        }), status
    
    except Exception as e:
        return jsonify({
            "errors": [{
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Ocurrió un error interno",
                "level": "error",
                "description": str(e)
            }]
        }), 500
    
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