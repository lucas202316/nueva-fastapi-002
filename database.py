import sqlite3

#conexión a la base de datos
ruta = r"C:\Lucas\bbdd\mi_api.db"
conexion = sqlite3.connect(
    ruta,
    check_same_thread=False
)
cursor = conexion.cursor()