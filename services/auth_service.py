import sqlite3
from schemas import Usuario
from repositories.user_repository import create_user
from auth import (
    hash_password,
    verify_password,
    create_access_token
)

def register_user(
    usuario: Usuario,
    db: sqlite3.Connection
):
    password_hash = hash_password(usuario.password)

    
    create_user(
        usuario,
        password_hash,
        db
    )


       

