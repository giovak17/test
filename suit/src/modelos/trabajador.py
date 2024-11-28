from dataclasses import dataclass
from typing import Optional
from src.db import db

atributos_trabajador = [
    "codigo",
    "nombre",
    "apellido_pat",
    "apellido_mat",
    "codigo_postal",
    "calle",
    "numero",
    "estado",
    "pais",
    "nombre_pc",
    "service_tag",
    "modelo",
    "fecha_inicio_garantia",
    "nombre_usuario",
    "pin",
    "password_pc",
    "usuario_dominio",
    "password_dominio",
    "departamento",
    "numero_telefonico",
    "anydesk",
    "correo",
    "password_correo",
    "forward_correo",
    "listas_distribucion",
    "usuario_sage",
    "password_sage",
    "usuario_proseries",
    "password_proseries",
    "pc_virtual",
    "usuario_vpn",
    "password_vpn",
    "usuario_cotizador",
    "ams360",
    "password_ams360",
    "horario_comida",
    "empresa",
]

# Es el nombre de los atributos cuando se devuelve o recibe un trabajador en formato JSON
atributos_trabajador_json = [
    "codigo",
    "nombre",
    "apellidopat",
    "apellidomat",
    "codigopostal",
    "calle",
    "numero",
    "estado",
    "pais",
    "nombrepc",
    "servicetag",
    "modelo",
    "fechainiciogarantia",
    "nombreusuario",
    "pin",
    "passwordpc",
    "usuariodominio",
    "passworddominio",
    "departamento",
    "numerotelefonico",
    "anydesk",
    "correo",
    "passwordcorreo",
    "forwardcorreo",
    "listasdistribucion",
    "usuariosage",
    "passwordsage",
    "usuarioproseries",
    "passwordproseries",
    "pcvirtual",
    "usuariovpn",
    "passwordvpn",
    "usuariocotizador",
    "ams360",
    "passwordams360",
    "horariocomida",
    "empresa",
]


@dataclass
class Trabajador:
    codigo: Optional[int] = None
    nombre: Optional[str] = None
    apellido_pat: Optional[str] = None
    apellido_mat: Optional[str] = None
    codigo_postal: Optional[str] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    estado: Optional[str] = None
    pais: Optional[str] = None
    nombre_pc: Optional[str] = None
    service_tag: Optional[str] = None
    modelo: Optional[str] = None
    fecha_inicio_garantia: Optional[str] = None
    nombre_usuario: Optional[str] = None
    pin: Optional[str] = None
    password_pc: Optional[str] = None
    usuario_dominio: Optional[str] = None
    password_dominio: Optional[str] = None
    departamento: Optional[str] = None
    numero_telefonico: Optional[str] = None
    anydesk: Optional[str] = None
    correo: Optional[str] = None
    password_correo: Optional[str] = None
    forward_correo: Optional[str] = None
    listas_distribucion: Optional[str] = None
    usuario_sage: Optional[str] = None
    password_sage: Optional[str] = None
    usuario_proseries: Optional[str] = None
    password_proseries: Optional[str] = None
    pc_virtual: Optional[str] = None
    usuario_vpn: Optional[str] = None
    password_vpn: Optional[str] = None
    usuario_cotizador: Optional[str] = None
    ams360: Optional[str] = None
    password_ams360: Optional[str] = None
    horario_comida: Optional[str] = None
    empresa: Optional[int] = None

    def registrar(self):
        sentencia = """
            INSERT INTO trabajadores
            (codigo, nombre, apellidopat, apellidomat, codigopostal, calle, numero, estado,
            pais, nombrepc, servicetag, modelo, fechainiciogarantia, nombreusuario, pin,
            passwordpc, usuariodominio, passworddominio, departamento, numerotelefonico,
            anydesk, correo, passwordcorreo, forwardcorreo, listasdistribucion, usuariosage,
            passwordsage, usuarioproseries, passwordproseries, pcvirtual, usuariovpn, passwordvpn,
            usuariocotizador, ams360, passwordams360, horariocomida, empresa)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s)
        """

        atributos = (*self.__dict__.values(),)

        try:
            codigo = db.execsql(sentencia, atributos)

            if not isinstance(codigo, int):
                raise Exception

            self.codigo = codigo

        except Exception as e:
            raise e

    def actualizar(self, codigo: int):
        # codigo es la primary key del trabajador que se desea actualizar mientras que self.codigo es el codigo(PK) actual del registro
        atributos = (*self.__dict__.values(), codigo)
        query = """
            UPDATE trabajadores
            SET
            codigo = %s, nombre = %s, apellidopat = %s, apellidomat = %s,
            codigopostal = %s, calle = %s, numero = %s, estado = %s,
            pais = %s, nombrepc = %s, servicetag = %s, modelo = %s,
            fechainiciogarantia = %s, nombreusuario = %s, pin = %s, passwordpc = %s,
            usuariodominio = %s, passworddominio = %s, departamento = %s, numerotelefonico = %s,
            anydesk = %s, correo = %s, passwordcorreo = %s, forwardcorreo = %s,
            listasdistribucion = %s, usuariosage = %s, passwordsage = %s, usuarioproseries = %s,
            passwordproseries = %s, pcvirtual = %s, usuariovpn = %s, passwordvpn = %s,
            usuariocotizador = %s, ams360 = %s, passwordams360 = %s, horariocomida = %s,
            empresa = %s
            WHERE codigo = %s;
        """
        try:
            db.execsql(query, atributos)
        except Exception as e:
            raise e

    def eliminar(self):
        try:
            db.execsql("DELETE FROM trabajadores WHERE codigo = %s", self.codigo)

        except Exception as e:
            raise e

    def obtener_json(self):
        trabajador_json = dict()

        for i in range(len(atributos_trabajador)):
            trabajador_json[atributos_trabajador_json[i]] = self.__dict__[
                atributos_trabajador[i]
            ]

        return trabajador_json
