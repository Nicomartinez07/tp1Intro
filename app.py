from flask import Flask, request, jsonify
import db

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/partidos", methods=["GET"])
def obtener_partidos():
    partidos = db.obtener_partidos()
    return jsonify(partidos)

@app.route("/partidos", methods=["POST"])
def crear_partido():


@app.route("/partidos/{id}", methods=["GET"])
def obtener_partido_por_id():

@app.route("/partidos/{id}", methods=["PUT"])
def reemplazar_partido():

@app.route("/partidos/{id}", methods=["PATCH"])
def actualizar_partido():

@app.route("/partidos", methods=["DELETE"])
def eliminar_partido():

@app.route("/partidos/{id}/resultado}", methods=["PUT"])
def actualizar_resultado_de_partido():

@app.route("/partidos/{id}/prediccion}", methods=["POST"])
def realizar_prediccion():

#Usuarios

@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():

@app.route("/usuarios", methods=["POST"])
def crear_usuario():

@app.route("/usuarios/{id}", methods=["GET"])
def obtener_usuario_por_id():

@app.route("/usuarios/{id}", methods=["PUT"])
def reemplazar_usuario():

@app.route("/usuarios/{id}", methods=["DELETE"])
def eliminar_usuario():

if __name__ == "__main__":
    app.run(debug=True)

