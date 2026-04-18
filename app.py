from flask import Flask, request, jsonify
import db
from routes.partido_router import partidos_bp
from routes.usuario_router import usuarios_bp
from routes.ranking_router import ranking_bp
import utils.error_handlers as error_handlers
import utils.middleware_hateoas as middleware

app = Flask(__name__)

middleware.start_hateoas(app)
error_handlers.start(app)

app.register_blueprint(partidos_bp, url_prefix="/partidos")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(ranking_bp, url_prefix="/ranking")

import sys
if __name__ == "__main__":
    port = 5000  # default

    if len(sys.argv) > 1: # si se pasa un argumento al ejecutar 'python app.py {numero_puerto}' se ejecuta en el puerto indicado 
        port = int(sys.argv[1])

    app.run(port=port, debug=True)

