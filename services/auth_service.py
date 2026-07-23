import sqlite3
from schemas import Usuario
from repositories.user_repository import create_user, get_user_by_email
from auth import (
    hash_password,
    verify_password,
    create_access_token
)
from exceptions import InvalidCredentialsError

def register_user(
    usuario: Usuario,
    db: sqlite3.Connection
):
    password_hash = hash_password(usuario.password)
    rol="user"
    
    create_user(
        usuario,
        password_hash,
        rol,
        db
        
    )
    return {
        "mensaje": "Usuario registrado"
    }

def login(
    db: sqlite3.Connection,
    email: str,
    password: str
):
    usuario = get_user_by_email(
    db,
    email
)

    if usuario is None:
                raise InvalidCredentialsError()
            
    password_guardada = usuario["password"]
    
    if not verify_password(
        password,
        password_guardada

    ):
        raise InvalidCredentialsError()
            
    token = create_access_token(
        usuario["id"],
        usuario["role"]
        )


        
    return {
            "access_token": token,
            "token_type": "bearer"

        }

            
    
    

