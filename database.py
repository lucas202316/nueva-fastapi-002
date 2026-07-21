import sqlite3
from config import DATABASE_PATH


def get_db():
    conexion = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )
    conexion.row_factory = sqlite3.Row #Sirve para que el cursor devuelva diccionarios en lugar de tuplas
    try:
        yield conexion
    finally:
        conexion.close()
