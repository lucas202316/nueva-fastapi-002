import sqlite3
from schemas import Usuario
from exceptions import UserAlreadyExistsError


def create_user(
    usuario: Usuario,
    password_hash: str,
    rol: str,
    db: sqlite3.Connection
    
):
    try:
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO usuarios(nombre, email, password, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                usuario.nombre,
                usuario.email,
                password_hash,
                rol
            )
        )

        db.commit()
    except sqlite3.IntegrityError:

        raise UserAlreadyExistsError()


def get_all_users(db: sqlite3.Connection):
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, nombre, email,role
        FROM usuarios
    """)

    usuarios = cursor.fetchall()

    resultado = []

    for usuario in usuarios:
        resultado.append({
            "id": usuario[0],
            "nombre": usuario[1],
            "email": usuario[2],
            "rol": usuario[3]
            
        })

    return resultado

def get_user_by_id(db: sqlite3.Connection, user_id: int):
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, nombre, email, role
        FROM usuarios
        WHERE id = ?
    """, (user_id,))

    usuario = cursor.fetchone()

    if usuario is None:
        return None

    return {
        "id": usuario[0],
        "nombre": usuario[1],
        "email": usuario[2],
        "rol": usuario[3]
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


    
    '''usuario = cursor.fetchone()

    if usuario is None:
        return None

    return dict(usuario)'''

def delete_user(db: sqlite3.Connection, user_id: int):
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM usuarios
        WHERE id = ?
    """, (user_id,))

    db.commit()

    return cursor.rowcount

def get_user_by_email(
    db: sqlite3.Connection,
    email: str
):
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT *
        FROM usuarios
        WHERE email = ?
        """,
        (email,)
    )

    return cursor.fetchone()
