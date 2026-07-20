#Es decir, el servicio no debería abrir una conexión nueva. Debería recibir la que FastAPI ya le entregó.
import sqlite3
from schemas import Usuario
from auth import hash_password
from repositories.user_repository import create_user


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
       
    
    


#SOLICITUDES
'''{
    "nombre":"Juan",
    "email":"juan@gmail.com",
    "password":"123456"
}'''
