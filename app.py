from flask import Flask, request, jsonify
import db
from routes.partido_router import partidos_bp
from routes.usuario_router import usuarios_bp
import utils.error_handlers as error_handlers
import utils.middleware_hateoas as middleware

app = Flask(__name__)

middleware.start_hateoas(app)
error_handlers.start(app)

app.register_blueprint(partidos_bp, url_prefix="/partidos")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")


@app.route("/ranking", methods=["GET"])
def obtener_ranking():
    try:
        conn = db.get_connection()
        cur = conn.cursor(dictionary=True)

        limit = request.args.get('_limit', default=10, type=int)
        offset = request.args.get('_offset', default=0, type=int)
        # compara predicciones a resultados
        # usando SIGN para determinar Ganador/Empate/Perdedor ¿?
        # ordena por puntos de manera descendiente para hacer un listado
        # limit y offset para paginar resultados
        query = """
            SELECT 
                p.usuario_id AS id_usuario,
                SUM(
                    CASE 
                        WHEN p.prediccion_local = r.goles_local AND p.prediccion_visitante = r.goles_visitante THEN 3
                        WHEN SIGN(p.prediccion_local - p.prediccion_visitante) = SIGN(r.goles_local - r.goles_visitante) THEN 1
                        ELSE 0 
                    END
                ) AS puntos
            FROM predicciones p
            INNER JOIN resultados r ON p.partido_id = r.partido_id
            GROUP BY p.usuario_id 
            ORDER BY puntos DESC, id_usuario ASC
            LIMIT %s OFFSET %s
        """
        cur.execute(query, (limit, offset))
        ranking = cur.fetchall()

        if not ranking:
            return "", 204 

        # Respuesta con HATEOAS
        respuesta = {
            "ranking": ranking,
            "_links": {
                "_first": {"href": f"https://www.hostname.com/prode_api?_offset=0&_limit={limit}"}, #
                "_prev":  {"href": f"https://www.hostname.com/prode_api?_offset={max(0, offset - limit)}&_limit={limit}"},
                "_next":  {"href": f"https://www.hostname.com/prode_api?_offset={offset + limit}&_limit={limit}"},
                "_last":  {"href": f"https://www.hostname.com/prode_api?_offset={offset}&_limit={limit}"} 
            }
        }
        return jsonify(respuesta), 200

    except Exception as e:
        return jsonify({
            "errors": [
                {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Ocurrió un error al obtener el ranking",
                    "level": "error",
                    "description": str(e)
                }
            ]
        }), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

import sys
if __name__ == "__main__":
    port = 5000  # default

    if len(sys.argv) > 1: # si se pasa un argumento al ejecutar 'python app.py {numero_puerto}' se ejecuta en el puerto indicado 
        port = int(sys.argv[1])

    app.run(port=port, debug=True)

