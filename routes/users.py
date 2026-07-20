from fastapi import APIRouter, Depends
import sqlite3
from schemas import Usuario
from database import conexion, cursor
from dependencies import get_current_user
from auth import hash_password

router = APIRouter()

#PERFIL/ruta protegida
@router.get("/profile")
def profile(usuario = Depends(get_current_user)):

    return usuario 

#REGISTRO
@router.post("/register")
def register(usuario: Usuario):
    
    password_hash = hash_password(usuario.password)
    
    try:
        cursor.execute(
            """
            INSERT INTO usuarios(nombre, email, password)
            VALUES (?, ?, ?)
            """,
            (
                usuario.nombre,
                usuario.email,
                password_hash #porque estaba en bytes y hay que pasarlo a texto
            )
        )
        conexion.commit()

    except sqlite3.IntegrityError:
        return {"mensaje": "El correo electrónico ya está registrado"}
    
    return {
            "mensaje": "Usuario registrado",
            "password_original": usuario.password,
            "password_hasheada": password_hash

        }


#SOLICITUDES
'''{
    "nombre":"Juan",
    "email":"juan@gmail.com",
    "password":"123456"
}'''
