from flask import Flask, request, jsonify, Blueprint
from multidict import MultiDict
import db
from routes.partido_router import partidos_bp
from routes.usuario_router import usuarios_bp

app = Flask(__name__)

app.register_blueprint(partidos_bp, url_prefix="/partidos")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

def build_HATEOAS_links(api_url, request_args, limit, offset, total):
    # Estos son los links que SIEMPRE van a estar
    base_links = {
        "self": {"href": f"{api_url}?{request_args}&_limit={limit}&_offset={offset}"},
        "first": {"href": f"{api_url}?{request_args}&_limit={limit}&_offset={0}"}, 
        "last":  {"href": f"{api_url}?{request_args}&_limit={limit}&_offset={max(((total - 1) // limit) * limit, 0)}"}
    }

    # si estamos en la primera pagina no existe un pagina anterior 
    if offset > 0:
        base_links["prev"] = {"href": f"{api_url}?{request_args}&_limit={limit}&_offset={max(offset-limit, 0)}"}

    # si estamos en la ultima pagina no existe una pagina siguiente
    if offset + limit < total: 
        base_links["next"] = {"href": f"{api_url}?{request_args}&_limit={limit}&_offset={min(offset+limit, total)}"}

    return base_links

def request_args_to_string(args: MultiDict[str, str]): # sin considerar _limit y _offset
    from urllib.parse import urlencode
    
    request_args = {}
    #Todos los parametros de la query aparte del _limit y _offset se agregan en un sring para la nueva response
    for arg, value in args.items():
        if arg not in ('_limit', '_offset'):
            request_args[arg] = value

    args_string = urlencode(request_args) # convierte el diccionario de parametros a un string con formato de query seguro para url ej: equipo=Argentina&fase=grupos

    return args_string

@app.after_request # funcion que se ejecuta despues de CUALQUIER request, osea despues de que se ejecuta la funcion en el router 
def aplicar_hateos(response): 
    print("hola soy el after_request y me ejecute", flush=True)
    NoEsUnGET = not request.method == "GET"
    NoEsJson = not response.is_json
    NoFueExitosa = not response.status_code == 200

    if NoEsUnGET or NoEsJson or NoFueExitosa:
        return response
    

    print("hola soy el after_request y pase todas las condiciones menos 'total'", flush=True)
    response_data = response.get_json()
    print("response_data: ", response, flush=True)

    # SI NO SE PASA EL CAMPO 'TOTAL' APARTE DE LA RESPUESTA DE LA REQUEST, NO SE ACTIVA EL HATEOAS 
    NoTieneCampoTotal = "total" not in response_data
    if NoTieneCampoTotal:
        return response
    
    print("hola soy el after_request y pase todas las condiciones", flush=True)

    total = response_data["total"] # total de resultados que hay en TODA la base de datos para ESA QUERY, sin considerar el limit. Osea todos los resultado que habria sin la paginacion
    limit = request.args.get('_limit', default=10, type=int)
    offset = request.args.get('_offset', default=0, type=int)

    request_args = request_args_to_string(request.args) # string con los parametros de la query  ej: ?equipo=Argentina&fase=grupos&

    api_url = request.base_url # devuelve http://127.0.0.1:5000/partidos/  sin los parametros 

    response_nueva = response_data
    response_nueva["_links"] = build_HATEOAS_links(api_url, request_args, limit, offset, total) # se agregan los links HATEOAS a la response original

    response.set_data(jsonify(response_nueva).get_data()) # remplaza la response original por la nueva response con HATEOAS

    return response

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

