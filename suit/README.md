# Backend Empresas - Trabajadores.

**Autor**: Barraza Andalon Kevin Giovanni

## Instrucciones.
### Instalacion y configuracion.
Es necesario tener **Python3** y **Pip** instalados.

1. Clonar el repositorio.

2. Crear un entorno virtual en la carpeta donde se clono el repositorio.
```bash
python3 -m venv .venv
```
3. Activar el entorno virtual.
```bash
# Linux / MacOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

4. Instalar los paquetes necesarios.
```bash
pip install -r requeriments.txt
```

5. Crear un archivo llamado ".env" para establecer las variables de conexion a la base de datos.
```bash
HOST=host
USER=user
PASSWORD=password
DATABASE=database
```

6. Para configurar el esquema de la base de datos, es necesario ejecutar el codigo SQL dentro del archivo ```database.sql```. Este archivo incluye datos de prueba para realizar tests con la API. Si se desea utilizar estos datos de prueba, sera necesario ejecutar las sentencias INSERT ubicadas al final del archivo.

7. Una vez completados los pasos anteriores, la API estara lista para iniciar. Para ello, utilice el siguiente comando:

```bash
gunicorn run:app -b 0.0.0.0:8000
```
```:8000``` es el puerto en el que se esta ejecutando, puede cambiarse si se asi se desea.


Si se requieren manejar multiples conexiones concurrentes, la API puede iniciarse con la siguiente configuracion:

```bash
gunicorn -w 9 --threads 4 run:app -b 0.0.0.0:8000
```

En este comando:

- ```-w 9``` representa la cantidad de procesos a utilizar.
- ```--threads 4``` indica la cantidad de hilos asignados para manejar las peticiones.

Se recomienda calcular el numero basico de procesos con la formula:
```(2 x CPUs) + 1```

Por ejemplo, en un equipo con 4 nucleos ```((2 x 4) + 1)```, se recomienda iniciar con 9 procesos para una aplicacion basica. Esta configuracion de 9 procesos y 4 hilos permite gestionar hasta 36 conexiones simultaneas. Ajuste el numero de procesos e hilos segun las necesidades de la aplicacion.


## Rutas
### Empresas

**GET** ```/api/empresas```

Obtener los datos de todas las empresas.

Ejemplo respuesta:
```200```

```json
{
  "datos": [
    {
      "calle": "Avenida Innovación",
      "codigoPostal": "12345",
      "estado": "Ciudad de México",
      "fechaRegistro": "Tue, 05 Nov 2024 20:22:39 GMT",
      "id": 1,
      "nombreComercial": "EcoTech Solutions",
      "numero": "101",
      "pais": "Mexico",
      "rfc": "ETC123456789",
      "tipoEmpresa": 1
    },
    {
      "calle": "Calle Verde",
      "codigoPostal": "54321",
      "estado": "Jalisco",
      "fechaRegistro": "Tue, 05 Nov 2024 20:22:39 GMT",
      "id": 2,
      "nombreComercial": "Green Horizons",
      "numero": "202",
      "pais": "Mexico",
      "rfc": "GHZ987654321",
      "tipoEmpresa": 2
    },
    ...
  ],
  "estatus": 0
}
```

\
**GET** ```/api/empresas/{id}```

Obtener los datos de una empresa segun su id.

Consulta empresa con ```id``` 1:

Ejemplo respuesta:
```200```

```json
{
  "datos": {
    "calle": "Avenida Innovación",
    "codigoPostal": "12345",
    "estado": "Ciudad de México",
    "fechaRegistro": "Tue, 05 Nov 2024 20:22:39 GMT",
    "id": 1,
    "nombreComercial": "EcoTech Solutions",
    "numero": "101",
    "pais": "Mexico",
    "rfc": "ETC123456789",
    "tipoEmpresa": 1
  },
  "estatus": 0
}
```

\
**GET** ```/api/empresas/{id}/trabajadores```

Obtener todos los trabajadores de una empresa.

Consulta los trabajadores de la empresa con ```id``` 1:

Ejemplo respuesta:
```200```

```json
{
  "datos": [
    {
      "apellidomat": "Lopez",
      "apellidopat": "Perez",
      "calle": "Av. Reforma",
      "codigo": 1,
      "codigopostal": "01234",
      "correo": "carlos.p@example.com",
      "estado": "CDMX",
      "modelo": "Dell Inspiron",
      "nombre": "Carlos",
      "nombrepc": "PC-Carlos",
      "numero": "123",
      "pais": "Mexico",
      "passwordcorreo": "emailpass1"
    },
    {
      "apellidomat": "Martinez",
      "apellidopat": "Gonzalez",
      "calle": "Calle 5",
      "codigo": 2,
      "codigopostal": "56789",
      "correo": "maria.g@example.com",
      "estado": "Jalisco",
      "modelo": "HP Pavilion",
      "nombre": "Maria",
      "nombrepc": "PC-Maria",
      "numero": "456",
      "pais": "Mexico",
      "passwordcorreo": "emailpass2"
    },
    ...
  ],
  "estatus": 0
}

```

Ejemplo respuesta:
```404```

```json
{
  "datos": [],
  "estatus": 1,
  "mensaje": "No existen trabajadores relacionados a la empresa con id: 1."
}
```

\
**GET** ```/api/empresas/usuario/{id}```
Obtener las empresas asignadas a un usuario.

Consulta las empresas asignadas al usuario con id ```4```:

Ejemplo respuesta:
```200```

```json
{
  "datos": [
    {
      "calle": "Avenida Innovación",
      "codigoPostal": "12345",
      "estado": "Ciudad de México",
      "fechaRegistro": "Sat, 09 Nov 2024 16:47:58 GMT",
      "id": 1,
      "nombreComercial": "EcoTech Solutions",
      "numero": "101",
      "pais": "Mexico",
      "rfc": "ETC123456789",
      "tipoEmpresa": 1
    },
    {
      "calle": "Calle Verde",
      "codigoPostal": "54321",
      "estado": "Jalisco",
      "fechaRegistro": "Sat, 09 Nov 2024 16:47:58 GMT",
      "id": 2,
      "nombreComercial": "Green Horizons",
      "numero": "202",
      "pais": "Mexico",
      "rfc": "GHZ987654321",
      "tipoEmpresa": 2
    },
    ...
  ],
  "estatus": 0
}
```

Ejemplo respuesta:
```404```

```json
{
  "datos": [],
  "estatus": 1,
  "mensaje": "Usuario con id: 4 no tienen empresas asignadas."
}

```

\
**POST** ```/api/empresas/```
Agregar empresa.

Datos de la peticion:
```json
Header: "Content-Type: application/json"
Body:
  {
    "calle": "Avenida Naciones",
    "codigoPostal": "22288",
    "estado": "Baja California",
    "nombreComercial": "BC Solutions",
    "numero": "204JC",
    "pais": "Mexico",
    "rfc": "BCS123456789",
    "tipoEmpresa": 1
  }
```

Ejemplo respuesta:
```201```

```json
{
  "estatus": 0,
  "id": 6,
  "mensaje": "Registro exitoso."
}
```

Ejemplo respuesta:
```500```

```json
{
  "error": "(1062, \"Duplicate entry 'BCS123456789' for key 'rfc'\")",
  "estatus": 1,
  "mensaje": "No se pudo registrar."
}
  
```

\
**PATCH** ```/api/empresas/{id}```

Actualizar los datos de una empresa de manera total o parcial.

Actualizar todos los datos de la empresa con ```id``` 6:

Datos de la peticion:
```json
Header: "Content-Type: application/json"
Body:
  { 
    "calle": "Calle Victoria", 
    "id": 6,
    "codigoPostal": "22293", 
    "estado": "Sonora", 
    "nombreComercial": "Sonora Tech", 
    "numero": "101JC", 
    "pais": "Mexico", 
    "rfc": "STC12345678A",
    "tipoEmpresa": 2
  }  
```

Ejemplo respuesta:
```200```

```json
{
  "datos": {
    "calle": "Calle Victoria",
    "codigoPostal": "22293",
    "estado": "Sonora",
    "fechaRegistro": "Thu, 07 Nov 2024 20:57:34 GMT",
    "id": 6,
    "nombreComercial": "Sonora Tech",
    "numero": "101JC",
    "pais": "Mexico",
    "rfc": "STC12345678A",
    "tipoEmpresa": 2
  },
  "estatus": 0,
  "mensaje": "Empresa actualizada de manera exitosa."
}
```

Actualizacion parcial de la empresa con ```id``` 6, por ejemplo, solo se desea cambiar el nombre comercial y codigo postal:

Datos de la peticion:
```json
Header: "Content-Type: application/json"
Body:
  { 
    "codigoPostal": "25511", 
    "nombreComercial": "Modern Tech"
  }

```

Ejemplo respuesta:
```200```

```json
{
  "datos": {
    "calle": "Calle Victoria",
    "codigoPostal": "25511",
    "estado": "Sonora",
    "fechaRegistro": "Thu, 07 Nov 2024 20:57:34 GMT",
    "id": 6,
    "nombreComercial": "Modern Tech",
    "numero": "101JC",
    "pais": "Mexico",
    "rfc": "STC12345678A",
    "tipoEmpresa": 2
  },
  "estatus": 0,
  "mensaje": "Empresa actualizada de manera exitosa."
}
```

Ejemplo respuesta:
```404```

```json
{
  "estatus": 1,
  "mensaje": "No existe ninguna empresa con id: 6."
}
```

\
**DELETE** ```/api/empresas/{id}```

Eliminar una empresa por id.

Eliminar empresa con ```id``` 6:

Ejemplo respuesta:
```200```

```json
{
  "estatus": 0,
  "mensaje": "Empresa eliminada de manera exitosa."
}
```

Ejemplo respuesta:
```404```

```json
{
  "estatus": 1,
  "mensaje": "No existe ninguna empresa con id: 6."
}
```

### Trabajadores

**GET** ```/api/trabajadores```

Obtener los datos de todos trabajadores.

Ejemplo respuesta:
```200```

```json
"datos": [
  {
    "ams360": "ams360user1",
    "anydesk": "AD-1234",
    "apellidomat": "Lopez",
    "apellidopat": "Perez",
    "calle": "Av. Reforma",
    "codigo": 1,
    "codigopostal": "01234",
    "correo": "carlos.p@example.com",
    "departamento": "IT",
    "empresa": 1,
    "estado": "CDMX",
    "fechainiciogarantia": "Wed, 13 Nov 2024 18:45:54 GMT",
    "forwardcorreo": "fwd@example.com",
    "horariocomida": "12:00-13:00",
    "listasdistribucion": "list1",
    "modelo": "Dell Inspiron",
    "nombre": "Carlos",
    "nombrepc": "PC-Carlos",
    "nombreusuario": "carlos.p",
    "numero": "123",
    "numerotelefonico": "5551234567",
    "pais": "Mexico",
    "passwordams360": "ams360pass1",
    "passwordcorreo": "emailpass1",
    "passworddominio": "dompass1",
    "passwordpc": "passpc1",
    "passwordproseries": "proseriespass1",
    "passwordsage": "sagepass1",
    "passwordvpn": "vpnpass1",
    "pcvirtual": "PC-Virtual",
    "pin": "1234",
    "servicetag": "ST12345",
    "usuariocotizador": "cotizador1",
    "usuariodominio": "domuser1",
    "usuarioproseries": "proseriesuser1",
    "usuariosage": "sageuser1",
    "usuariovpn": "vpnuser1"
  } 
  ...
 ]
```

\
**GET** ```/api/trabajadores/{codigo}```

Obtener los datos de un trabajador segun su codigo. Solo se devuelven los datos de acorde al tipo de empresa.

Consulta trabajador con ```codigo``` 2:

Ejemplo respuesta:
```200```

```json
{
  "datos": {
    "apellidomat": "Martinez",
    "apellidopat": "Gonzalez",
    "calle": "Calle 5",
    "codigo": 2,
    "codigopostal": "56789",
    "correo": "maria.g@example.com",
    "empresa": 1,
    "estado": "Jalisco",
    "modelo": "HP Pavilion",
    "nombre": "Maria",
    "nombrepc": "PC-Maria",
    "numero": "456",
    "pais": "Mexico",
    "passwordcorreo": "emailpass2"
  },
  "estatus": 0
}
```

Ejemplo respuesta:
```404```

```json
{
  "estatus": 1,
  "mensaje": "No existe ningun trabajador con codigo: 2."
}
```

\
**GET** ```/api/trabajadores/buscar?nombre={string}```
Buscar trabajador por nombre, apellido paterno o materno donde ```string``` es el nombre o apellido del trabajador a buscar.

Buscar trabajador llamado carlos:

Ejemplo respuesta:
```200```

```json
{
  "datos": {
    "apellidomat": "Lopez",
    "apellidopat": "Perez",
    "calle": "Av. Reforma",
    "codigo": 1,
    "codigopostal": "01234",
    "correo": "carlos.p@example.com",
    "empresa": 1,
    "estado": "CDMX",
    "modelo": "Dell Inspiron",
    "nombre": "Carlos",
    "nombrepc": "PC-Carlos",
    "numero": "123",
    "pais": "Mexico",
    "passwordcorreo": "emailpass1"
  },
  "estatus": 0
}
```

Ejemplo respuesta:
```400```

```json
{
  "estatus": 1,
  "mensaje": "La busqueda requiere que 'nombre' contenga un valor."
}
```

Ejemplo respuesta:
```404```

```json
{
  "datos": [],
  "estatus": 1,
  "mensaje": "No se encontraron resultados."
}
```

\
**POST** ```/api/trabajadores```
Registrar trabajador. Se registra el trabajador con los datos adecuados segun el tipo de empresa.

Datos de la peticion:
```json
Header: "Content-Type: application/json"
Body:
{ 
  "nombre": "Joaquin",
  "apellidopat": "Camacho",
  "apellidomat": "Martinez",
  "calle": "Calle Independencia",
  "codigopostal": "33222",
  "correo": "camachomj.p@tech.com",
  "empresa": 1,
  "estado": "CDMX",
  "modelo": "Lenovo Thinkpad",
  "nombrepc": "PC-Joaquin",
  "numero": "444",
  "pais": "Mexico",
  "passwordcorreo": "joaquin123"
}
```

Ejemplo respuesta:
```201```

```json
{
  "codigo": 11,
  "estatus": 0,
  "mensaje": "Registro exitoso."
}
```

\
**PATCH** ```/api/trabajadores/{codigo}```
Actualizar los datos de un trabajador de manera total o parcial.

Actualizar todos los datos del trabajador con ```codigo``` 11:

Datos de la peticion:
```json
Header: "Content-Type: application/json"
Body:
{ 
  "nombre": "Gonzalo",
  "apellidopat": "Herrera",
  "apellidomat": "Garcia",
  "calle": "Calle Innovacion",
  "codigopostal": "22211",
  "correo": "herreragj.p@tech.com",
  "empresa": 1,
  "estado": "CDMX",
  "modelo": "Lenovo Ideapad",
  "nombrepc": "PC-Gonzalo",
  "numero": "444",
  "pais": "Mexico",
  "passwordcorreo": "gonzalo77"
}
```

Ejemplo respuesta:
```200```

```json
{
  "estatus": 0,
  "mensaje": "Trabajador actualizado de manera exitosa."
}

```

Actualizacion parcial del trabajador con ```codigo``` 11, por ejemplo, solo se desea cambiar el apellido paterno y el codigo postal:

Datos de la peticion:
```json
Header: "Content-Type: application/json"
Body:
{ 
  "apellidopat": "Hernandez",
  "codigopostal": "22289"
}

```

Ejemplo respuesta:
```200```

```json
{
  "estatus": 0,
  "mensaje": "Trabajador actualizado de manera exitosa."
}
```

Ejemplo respuesta:
```404```

```json
{
  "estatus": 1,
  "mensaje": "No existe ningun trabajador con codigo: 11."
```

\
**DELETE** ```/api/trabajadores/{codigo}```

Eliminar un trabajador por id.

Eliminar trabajador con ```codigo``` 11:

Ejemplo respuesta:
```200```

```json
{
  "estatus": 0,
  "mensaje": "Trabajador eliminado de manera exitosa."
}
```

Ejemplo respuesta:
```404```

```json
{
  "estatus": 1,
  "mensaje": "No existe ningun trabajador con codigo: 11."

}

```

