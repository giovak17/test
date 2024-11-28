from flask import Flask, Blueprint, redirect
from src.rutas.empresas import empresas
from src.rutas.trabajadores import trabajadores
from src.db import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# En caso de que se desee restringir el accesso al API agregar los sitios aceptados en origins
# CORS(app, origins=["https://ejemplo.com", "https://sitio.com"])


# Anadir prefijo '/api' a cada ruta
api_bp = Blueprint("api", __name__, url_prefix="/api")

# Registrar endpoints de rutas para empresass y trabajadores
api_bp.register_blueprint(empresas)
api_bp.register_blueprint(trabajadores)
app.register_blueprint(api_bp)


@app.route("/")
def root():
    return redirect("/api")


# Esta ruta checa la salud de la API y la base de datos
@app.route("/api")
def home():
    try:
        result = db.execsql("SELECT NOW()")
        if isinstance(result, int):
            return {}
    except Exception as e:
        return {
            "estatus": 1,
            "estado": {"db": "No disponible."},
            "error": e.__str__(),
        }, 500

    return {
        "estatus": 0,
        "estado": {
            "api": "OK",
            "db": "OK",
        },
        "tiempo": result[0],
    }, 200


# Comando para iniciar la API:
# gunicorn run:app -b 0.0.0.0:8000
if __name__ == "__main__":
    app.run()
    # Si se desea activar el modo debugging para hacer pruebas quitar comentario de esta linea
    # app.run(debug=True, port=8000)
