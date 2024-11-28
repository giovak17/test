from flask import Blueprint, request
from src.modelos.trabajador import Trabajador
from src.modelos.empresa import Empresa
from src.modelos.trabajador import atributos_trabajador
from src.modelos.trabajador import atributos_trabajador_json
from src.db import db

trabajadores = Blueprint("trabajadores", __name__, url_prefix="/trabajadores")


campos_obligatorios = [
    "codigo",
    "nombre",
    "apellidopat",
    "apellidomat",
    "pais",
    "estado",
    "codigopostal",
    "calle",
    "numero",
    "empresa",
]

# GET


# Esta ruta devolvera todos los trabajadores de todas las obtener_empresas. La cantidad de resultados
# puede ser limitada si se establece 'limite' como paramtetro de query al realizar la peticion.
@trabajadores.route("/", methods=["GET"])
def obtener_trabajadores():
    limite = request.args.get("limite", default=1000, type=int)

    try:
        trabajadores = db.execsql("SELECT * FROM trabajadores LIMIT %s", limite)
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "Solicitud no exitosa, por favor intente mas tarde.",
            "error": e.__str__(),
        }, 500

    return {"estatus": 0, "datos": trabajadores}


@trabajadores.route("/<int:codigo>", methods=["GET"])
def obtener_por_codigo(codigo):
    try:
        trabajador = db.execsql("SELECT * FROM trabajadores WHERE codigo = %s", codigo)

    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "Solicitud no exitosa, por favor intente mas tarde.",
            "error": e.__str__(),
        }, 500

    if isinstance(trabajador, int):
        return {}

    if len(trabajador) <= 0:
        return {
            "estatus": 1,
            "mensaje": f"No existe ningun trabajador con codigo: {codigo}.",
        }, 404

    trabajador_dict = trabajador[0]
    empresa_perteneciente_id = int(trabajador_dict["empresa"])

    try:
        empresa_perteneciente = Empresa(id=empresa_perteneciente_id)
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "Solicitud no exitosa, el trabajador no pertenece a ninguna empresa.",
            "error": e.__str__(),
        }, 500

    lista_campos = empresa_perteneciente.obtener_campos_tipo_empresa()

    for campo in campos_obligatorios:
        lista_campos.append(campo)

    # Filtrar los campos y que solo devuelva el empleado con los datos que le corresponden segun su tipo de empresa
    trabajador_dict_keys = list(trabajador_dict.keys())
    for key in trabajador_dict_keys:
        if key not in lista_campos:
            del trabajador_dict[key]

    return {"estatus": 0, "datos": trabajador_dict}, 200


@trabajadores.route("/buscar", methods=["GET"])
def buscar_por_nombre():
    nombre = request.args.get("nombre")

    if not bool(nombre):
        return {
            "estatus": 1,
            "mensaje": "La busqueda requiere que 'nombre' contenga un valor.",
        }, 400

    nombre_query = f"%{nombre}%"

    try:
        query = """
            SELECT * FROM trabajadores
            WHERE LOWER(nombre) LIKE LOWER(%s) OR 
            LOWER(apellidopat) LIKE LOWER(%s) OR
            LOWER(apellidomat) LIKE LOWER(%s)
            """
        trabajador = db.execsql(
            query,
            (
                nombre_query,
                nombre_query,
                nombre_query,
            ),
        )

    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "Solicitud no exitosa, por favor intente mas tarde.",
            "error": e.__str__(),
        }, 500

    if isinstance(trabajador, int):
        return {}

    if len(trabajador) <= 0:
        return {
            "estatus": 1,
            "mensaje": "No se encontraron resultados.",
            "datos": [],
        }, 404

    # Esta parte se asegura de que solo se devuelvan los datos corespondientes al tipo de empresa
    trabajador_dict = trabajador[0]
    empresa_perteneciente_id = int(trabajador_dict["empresa"])

    try:
        empresa_perteneciente = Empresa(id=empresa_perteneciente_id)
    except Exception:
        return {}, 500

    lista_campos = empresa_perteneciente.obtener_campos_tipo_empresa()

    for campo in campos_obligatorios:
        lista_campos.append(campo)

    # Filtrar los campos y que solo devuelva el empleado con los datos que le corresponden segun su tipo de empresa
    trabajador_dict_keys = list(trabajador_dict.keys())
    for key in trabajador_dict_keys:
        if key not in lista_campos:
            del trabajador_dict[key]

    return {"estatus": 0, "datos": trabajador_dict}, 200


# POST
@trabajadores.route("/", methods=["POST"])
def registrar():
    try:
        datos = request.get_json()
    except Exception:
        return {"estatus": 1, "mensaje": "JSON formado incorrectamente."}, 400

    trabajador = Trabajador()

    try:
        for i in range(len(atributos_trabajador)):
            setattr(
                trabajador,
                atributos_trabajador[i],
                datos.get(atributos_trabajador_json[i]),
            )

    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "Asegurese que el tipo de datos de los campos sea el correcto.",
            "error": e.__str__(),
        }, 400

    try:
        trabajador.registrar()
        return {
            "estatus": 0,
            "codigo": trabajador.codigo,
            "mensaje": "Registro exitoso.",
        }, 201
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "No se pudo registrar.",
            "error": e.__str__(),
        }, 500


# PATCH
@trabajadores.route("/<int:codigo_trabajador>", methods=["PATCH"])
def actualizar(codigo_trabajador: int):
    try:
        datos_request = request.get_json()
    except Exception:
        return {"estatus": 1, "mensaje": "JSON formado incorrectamente."}, 400

    try:
        trabajador_existente = db.execsql(
            "SELECT * FROM trabajadores WHERE codigo = %s", codigo_trabajador
        )
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "Solicitud no exitosa, por favor intenta mas tarde.",
            "error": e.__str__(),
        }, 500

    trabajador_a_actualizar = Trabajador()
    if isinstance(trabajador_existente, int):
        return {}

    if len(trabajador_existente) <= 0:
        return {
            "estatus": 1,
            "mensaje": f"No existe ningun trabajador con codigo: {codigo_trabajador}.",
        }, 404

    trabajador_existente = trabajador_existente[0]

    # Itera sobre la lista de atributos de la clase trabajador, para mappear los valores del trabajador existente a
    # la nueva instancia de Trabajador (trabajador_a_actualizar) y sobreescribir los unicamente los valores
    # que se desee actualizar.
    for i in range(len(atributos_trabajador)):
        setattr(
            trabajador_a_actualizar,
            atributos_trabajador[i],
            trabajador_existente[atributos_trabajador_json[i]],
        )

    for i in range(len(atributos_trabajador)):
        try:
            setattr(
                trabajador_a_actualizar,
                atributos_trabajador[i],
                datos_request[atributos_trabajador_json[i]],
            )
        except Exception:
            pass

    try:
        trabajador_a_actualizar.actualizar(codigo_trabajador)
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "No se pudo actualizar, por favor intente mas tarde.",
            "error": e.__str__(),
        }, 500

    return {
        "estatus": 0,
        # "datos": trabajador_a_actualizar.obtener_json(),
        "mensaje": "Trabajador actualizado de manera exitosa.",
    }, 200


@trabajadores.route("/<int:codigo>", methods=["DELETE"])
def eliminar(codigo):
    try:
        empresa_existente = db.execsql(
            "SELECT * FROM trabajadores WHERE codigo = %s", codigo
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
            "mensaje": f"No existe ningun trabajador con codigo: {codigo}.",
        }, 404

    trabajador = Trabajador(codigo=int(codigo))
    try:
        trabajador.eliminar()
    except Exception as e:
        return {
            "estatus": 1,
            "mensaje": "No se pudo eliminar.",
            "error": e.__str__(),
        }

    return {"estatus": 0, "mensaje": "Trabajador eliminado de manera exitosa."}
