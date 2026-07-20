#El Service responde: ¿Qué quiero hacer? Registrar usuario.
#El Repository responde: ¿Cómo hablo con la base de datos para hacerlo? INSERT INTO usuarios (...)
import sqlite3
from schemas import Usuario
from exceptions import UserAlreadyExistsError

#función que representa una operación sobre la tabla usuarios
#no crea conexiones las recibe en db:sqlite3.Connection
def create_user(usuario: Usuario,
                password_hash: str,
                db: sqlite3.Connection
):  
    try:
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO usuarios(nombre, email, password)
            VALUES (?, ?, ?)
            """,
            (
                usuario.nombre,
                usuario.email,
                password_hash
            )
        )

        db.commit()

    except sqlite3.IntegrityError:

        raise UserAlreadyExistsError()

#Cada operación sobre la base de datos debe utiliza su propio cursor
def get_all_users(db: sqlite3.Connection):
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, nombre, email
        FROM usuarios
    """)

    return cursor.fetchall()#lista de tuplas PERO DEBEMOS DEVOLVER DICCIONARIOS
