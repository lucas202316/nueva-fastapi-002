import sqlite3
from repositories import user_repository
from exceptions import UserNotFoundError


def get_all_users(db: sqlite3.Connection):
    return user_repository.get_all_users(db)

def get_user_by_id(db: sqlite3.Connection, user_id: int):
    usuario = user_repository.get_user_by_id(db, user_id)

    if usuario is None:
        raise UserNotFoundError()

    return usuario

def update_user(
    db: sqlite3.Connection,
    user_id: int,
    nombre: str,
    email: str
):
    filas_actualizadas = user_repository.update_user(
        db,
        user_id,
        nombre,
        email
    )

    if filas_actualizadas == 0:
        raise UserNotFoundError()

def delete_user(
    db: sqlite3.Connection,
    user_id: int
):
    filas_eliminadas = user_repository.delete_user(
        db,
        user_id
    )

    if filas_eliminadas == 0:
        raise UserNotFoundError()
  
