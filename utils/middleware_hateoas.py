from flask import request, jsonify
from urllib.parse import urlencode
from multidict import MultiDict

def build_HATEOAS_links(api_url, request_args, limit, offset, total):
    # Estos son los links que SIEMPRE van a estar
    base_links = {
        "_self": {"href": f"{api_url}?{request_args}&_limit={limit}&_offset={offset}"},
        "_first": {"href": f"{api_url}?{request_args}&_limit={limit}&_offset={0}"},
        "_last":  {"href": f"{api_url}?{request_args}&_limit={limit}&_offset={max(((total - 1) // limit) * limit, 0)}"}
    }

    if offset > 0:
        base_links["_prev"] = {"href": f"{api_url}?{request_args}&_limit={limit}&_offset={max(offset-limit, 0)}"}

    if offset + limit < total:
        base_links["_next"] = {"href": f"{api_url}?{request_args}&_limit={limit}&_offset={min(offset+limit, total)}"}

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




def start_hateoas(app):
    @app.after_request # funcion que se ejecuta despues de CUALQUIER request, osea despues de que se ejecuta la funcion en el router 
    def aplicar_hateos(response): 
        NoEsUnGET = not request.method == "GET"
        NoEsJson = not response.is_json
        NoFueExitosa = not response.status_code == 200

        if NoEsUnGET or NoEsJson or NoFueExitosa:
            return response

        response_data = response.get_json()

        # SI NO SE PASA EL CAMPO 'TOTAL' APARTE DE LA RESPUESTA DE LA REQUEST, NO SE ACTIVA EL HATEOAS 
        NoTieneCampoTotal = "total" not in response_data
        if NoTieneCampoTotal:
            return response

        total = response_data["total"] # total de resultados que hay en TODA la base de datos para ESA QUERY, sin considerar el limit. Osea todos los resultado que habria sin la paginacion
        limit = request.args.get('_limit', default=10, type=int)
        offset = request.args.get('_offset', default=0, type=int)

        request_args = request_args_to_string(request.args) # string con los parametros de la query  ej: ?equipo=Argentina&fase=grupos&

        api_url = request.base_url # devuelve http://127.0.0.1:5000/partidos/  sin los parametros 

        response_nueva = response_data
        response_nueva["_links"] = build_HATEOAS_links(api_url, request_args, limit, offset, total) # se agregan los links HATEOAS a la response original

        response.set_data(jsonify(response_nueva).get_data()) # remplaza la response original por la nueva response con HATEOAS

        return response