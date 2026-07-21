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


    usuarios = cursor.fetchall()

    resultado = []

    for usuario in usuarios:
        resultado.append({
            "id": usuario[0],
            "nombre": usuario[1],
            "email": usuario[2]
        })

    return resultado #ANTES DEVOLVIA LISTA DE TUPLAS AHORA MEJOR DEVUELVE DICCIONARIOS

def get_user_by_id(db: sqlite3.Connection, user_id: int):
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, nombre, email
        FROM usuarios
        WHERE id = ?
    """, (user_id,))

    usuario = cursor.fetchone()

    if usuario is None:
        return None

    return {
        "id": usuario[0],
        "nombre": usuario[1],
        "email": usuario[2]
        
        
    }

def update_user(
    db: sqlite3.Connection,
    user_id: int,
    nombre: str,
    email: str
):
    cursor = db.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET nombre = ?, email = ?
        WHERE id = ?
    """, (nombre, email, user_id))

    db.commit()
    return get_user_by_id(
        db,
        user_id
    )


    

def delete_user(db: sqlite3.Connection, user_id: int):
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM usuarios
        WHERE id = ?
    """, (user_id,))

    db.commit()

    return cursor.rowcount
