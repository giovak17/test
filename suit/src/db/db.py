import pymysql.cursors
from dotenv import load_dotenv
import os

_ = load_dotenv()  # Carga variables de entorno del archivo .env.


def connectar():
    return pymysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD", ""),
        database=os.getenv("DATABASE"),
        cursorclass=pymysql.cursors.DictCursor,
    )


def execsql(sql: str, arguments: object | None = None):
    """
    Permite ejectuar sentencias SQL.
    \nPrimer parametro: sentencia SQL.
    Segundo parametro (opcional): Tupla de argumentos para la sentencia en caso de que se trate de un prepared statement.
    Si se ejecuta SELECT u otra sentencia devuelve una lista con los resultados.
    Si se ejecuta INSERT devuelve el ID del ultimo registro insertado.
    """
    with connectar() as connection:
        with connection.cursor() as cursor:
            if arguments:
                try:
                    cursor.execute(sql, arguments)
                except Exception as e:
                    raise e
            else:
                try:
                    cursor.execute(sql)
                except Exception as e:
                    raise e
            connection.commit()
            if "insert into" in sql.lower():
                return cursor.lastrowid
            else:
                return cursor.fetchall()
