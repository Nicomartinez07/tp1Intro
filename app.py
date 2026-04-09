from flask import Flask, request, jsonify, Blueprint
import db

app = Flask(__name__)

partidos_bp = Blueprint("partidos", __name__, url_prefix="/partidos")
usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")

app.register_blueprint(partidos_bp)
app.register_blueprint(usuarios_bp)

@app.route("/ranking", methods=["GET"])s
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
    finally: 
        if conn:
            conn.close()
        if cur:
            cur.close()

if __name__ == "__main__":
    app.run(debug=True)

