from src.db import db
from dataclasses import dataclass
from typing import Optional

atributos_empresa = [
    "id",
    "nombre_comercial",
    "rfc",
    "codigo_postal",
    "calle",
    "numero",
    "estado",
    "pais",
    "fecha_registro",
    "tipo_empresa",
]
atributos_empresa_json = [
    "id",
    "nombreComercial",
    "rfc",
    "codigoPostal",
    "calle",
    "numero",
    "estado",
    "pais",
    "fechaRegistro",
    "tipoEmpresa",
]


@dataclass
class Empresa:
    id: Optional[int] = None
    nombre_comercial: Optional[str] = None
    rfc: Optional[str] = None
    codigo_postal: Optional[str] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    estado: Optional[str] = None
    pais: Optional[str] = None
    fecha_registro: Optional[str] = None
    tipo_empresa: Optional[int] = None

    def registrar(self):
        try:
            # id = db.execsql("INSERT INTO empresas (nombreComercial, rfc, codigoPostal, calle, numero, estado, pais, tipoEmpresa)\
            # VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            # (self.nombre_comercial, self.rfc, self.codigo_postal, self.calle, self.numero, self.estado, self.pais, self.tipo_empresa))
            sentencia = """
                INSERT INTO empresas (id, nombreComercial, rfc, codigoPostal, calle, numero, estado, pais, fechaRegistro, tipoEmpresa)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            id = db.execsql(sentencia, (*self.__dict__.values(),))

            if not isinstance(id, int):
                raise Exception

            self.id = id

        except Exception as e:
            raise e

    def actualizar(self, empresa_id: int):
        # empresa_id es el id de la empresa que se desea actualizar mientras que self.id es el id actual del registro
        query = """
            UPDATE empresas 
            SET id = %s, nombreComercial= %s, rfc = %s,
                codigoPostal = %s, calle = %s, numero = %s,
                estado = %s, pais = %s, fechaRegistro = %s, tipoEmpresa = %s
            WHERE id = %s
            """
        try:
            db.execsql(query, (*self.__dict__.values(), empresa_id))
        except Exception as e:
            raise e

    def eliminar(self):
        try:
            db.execsql("DELETE FROM empresas WHERE id = %s", self.id)

        except Exception as e:
            raise e

    def obtener_json(self):
        empresa_json = dict()

        for i in range(len(atributos_empresa)):
            empresa_json[atributos_empresa_json[i]] = self.__dict__[
                atributos_empresa[i]
            ]

        return empresa_json

    def obtener_campos_tipo_empresa(self) -> list[str]:
        """
        Devuelve una lista de campos/opciones que una empresa utiliza
        segun su tipo de empresa.
        Recibe el id de la empresa como argumento.
        """

        query = """
            SELECT DISTINCT lower(te.Opciones) as campos
            FROM trabajadores as t
            INNER JOIN empresas as emp
            ON t.empresa = emp.id
            INNER JOIN TiposEmpresas as te
            ON te.Numero = emp.tipoEmpresa
            WHERE emp.id = %s;
        """
        resultado = db.execsql(query, self.id)
        campost_tipo_empleado: str

        if isinstance(resultado, int):
            return [""]

        campost_tipo_empleado = resultado[0]["campos"]
        campost_tipo_empleado = campost_tipo_empleado.replace(" ", "").replace("_", "")
        listaCampos = campost_tipo_empleado.split(",")

        return listaCampos

    def obtener_trabajadores(self):
        campos_str = ""
        if isinstance(self.id, int):
            try:
                lista_campos = self.obtener_campos_tipo_empresa()
                campos_str = ", ".join(lista_campos)
            except Exception as e:
                raise e

        # query = f"""
        #    SELECT codigo, concat(ifnull(nombre, ''), ' ', ifnull(apellidopat, ''), ' ', ifnull(apellidomat, '')) AS nombre,
        #    CONCAT(pais, ', ', estado, ', ', codigopostal, ', ', calle, ', #', numero ) AS ubicacion,
        #    {campos_str}
        #    FROM trabajadores
        #    WHERE empresa = %s;
        # """

        query = f"""
            SELECT codigo, nombre, apellidopat, apellidomat, pais, estado, codigopostal, calle, numero,
            {campos_str}
            FROM trabajadores
            WHERE empresa = %s;
        """

        try:
            return db.execsql(query, self.id)
        except Exception as e:
            raise e
