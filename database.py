import sqlite3
from config import DATABASE_PATH
#conexión a la base de datos

def get_db():
    conexion = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )
    conexion.row_factory = sqlite3.Row
    try:
        yield conexion
    finally:
        conexion.close()
