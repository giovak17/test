from flask import Blueprint, request
from src.modelos.empresa import Empresa
from src.modelos.empresa import atributos_empresa
from src.modelos.empresa import atributos_empresa_json
from src.db import db

empresas = Blueprint("empresas", __name__, url_prefix="/empresas")

# GET


# Esta ruta devuelve todas las empresas existentes, la cantidad de resultados se puede limitar
# si se establece 'limite' como query parameter al realizar la peticion
@empresas.route("/", methods=["GET"])
def obtener_empresas():
    limite = request.args.get("limite", default=1000, type=int)

    try:
        empresas = db.execsql("SELECT * FROM empresas LIMIT %s", limite)
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "Solicitud no exitosa, por favor intente mas tarde.",
            "error": e.__str__(),
        }, 500

    return {"estatus": 0, "datos": empresas}


@empresas.route("/<int:empresa_id>", methods=["GET"])
def obtener_por_id(empresa_id):
    try:
        empresa = db.execsql("SELECT * FROM empresas WHERE id = %s", empresa_id)
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "Solicitud no exitosa, por favor intente mas tarde.",
            "error": e.__str__(),
        }, 500

    if not isinstance(empresa, int):
        if len(empresa) > 0:
            return {"estatus": 0, "datos": empresa[0]}

    return {
        "estatus": 1,
        "mensaje": f"No existe ninguna empresa con id: {empresa_id}.",
    }, 404


# Obtener todos los trabajadores segun la empresa
@empresas.route("/<int:empresa_id>/trabajadores", methods=["GET"])
def obtener_trabajadores(empresa_id):
    empresa = Empresa(id=empresa_id)

    try:
        trabajadores = empresa.obtener_trabajadores()

    except Exception:
        return {
            "estatus": 1,
            "mensaje": f"No existen trabajadores relacionados a la empresa con id: {empresa_id}.",
            "datos": [],
        }, 404

    return {"estatus": 0, "datos": trabajadores}, 200


# Obtener todas las empresas asignadas a un usuario
@empresas.route("/usuario/<int:usuario_id>", methods=["GET"])
def obtener_empresas_por_usuario(usuario_id):
    query = """
        SELECT id, nombreComercial, rfc, codigoPostal, calle, numero, estado, pais, fechaRegistro, tipoEmpresa
        FROM empresas
        INNER JOIN usuarios_empresas ue on empresas.id = ue.empresa
        WHERE ue.usuario = %s;
    """
    try:
        empresas = db.execsql(query, usuario_id)
        if isinstance(empresas, int):
            return {}

        if len(empresas) == 0:
            return {
                "estatus": 1,
                "mensaje": f"Usuario con id: {usuario_id} no tienen empresas asignadas.",
                "datos": empresas,
            }, 404

    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "Solicitud no exitosa, por favor intente mas tarde.",
            "error": e.__str__(),
        }, 500

    return {"estatus": 0, "datos": empresas}, 200


# POST
@empresas.route("/", methods=["POST"])
def agregar():
    try:
        datos = request.get_json()
    except Exception:
        return {"estatus": 1, "mensaje": "JSON formado incorrectamente."}, 400

    empresa = Empresa()

    try:
        for i in range(len(atributos_empresa)):
            setattr(
                empresa,
                atributos_empresa[i],
                datos.get(atributos_empresa_json[i]),
            )

    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": f"{e.args} es un campo requerido. Favor de asignarle un valor.",
        }, 400

    try:
        empresa.registrar()
        return {
            "estatus": 0,
            "id": empresa.id,
            "mensaje": "Registro exitoso.",
        }, 201
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "No se pudo registrar.",
            "error": e.__str__(),
        }, 500


# PATCH
@empresas.route("/<int:empresa_id>", methods=["PATCH"])
def actualizar(empresa_id):
    try:
        datos_request = request.get_json()
    except Exception:
        return {"estatus": 1, "mensaje": "JSON formado incorrectamente."}, 400

    try:
        empresa_existente = db.execsql(
            "SELECT * FROM empresas WHERE id = %s", empresa_id
        )
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "Solicitud no exitosa, por favor intenta mas tarde.",
            "error": e.__str__(),
        }, 500

    empresa_a_actualizar = Empresa()
    if isinstance(empresa_existente, int):
        return {}

    if len(empresa_existente) <= 0:
        return {
            "estatus": 1,
            "mensaje": f"No existe ninguna empresa con id: {empresa_id}.",
        }, 404

    empresa_existente = empresa_existente[0]

    # Asigna a la empresa vacia los atributos de la empresa existente
    for i in range(len(atributos_empresa)):
        setattr(
            empresa_a_actualizar,
            atributos_empresa[i],
            empresa_existente[atributos_empresa_json[i]],
        )

    # Asigna la empresa con los atributos de la empresa existente
    # los nuevos datos enviados en la peticion
    for i in range(len(atributos_empresa)):
        try:
            setattr(
                empresa_a_actualizar,
                atributos_empresa[i],
                datos_request[atributos_empresa_json[i]],
            )
        except Exception:
            pass

    try:
        empresa_a_actualizar.actualizar(empresa_id)
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "No se pudo actualizar, por favor intente mas tarde.",
            "error": e.__str__(),
        }, 500

    return {
        "estatus": 0,
        "datos": empresa_a_actualizar.obtener_json(),
        "mensaje": "Empresa actualizada de manera exitosa.",
    }, 200


# DELETE
@empresas.route("/<int:empresa_id>", methods=["DELETE"])
def eliminar(empresa_id):
    try:
        empresa_existente = db.execsql(
            "SELECT * FROM empresas WHERE id = %s", empresa_id
        )
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "Solicitud no exitosa, por favor intente mas tarde.",
            "error": e.__str__(),
        }, 500

    if isinstance(empresa_existente, int):
        return {}

    if len(empresa_existente) <= 0:
        return {
            "estatus": 1,
            "mensaje": f"No existe ninguna empresa con id: {empresa_id}.",
        }, 404

    empresa = Empresa(id=int(empresa_id))
    try:
        empresa.eliminar()
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "No se pudo eliminar.",
            "error": e.__str__(),
        }

    return {"estatus": 0, "mensaje": "Empresa eliminada de manera exitosa."}
