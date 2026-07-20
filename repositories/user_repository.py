#El Service responde: ¿Qué quiero hacer? Registrar usuario.
#El Repository responde: ¿Cómo hablo con la base de datos para hacerlo? INSERT INTO usuarios (...)
import sqlite3
from schemas import Usuario
from exceptions import UserAlreadyExistsError

#función que representa una operación sobre la tabla usuarios
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
