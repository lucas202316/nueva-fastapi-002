from fastapi import APIRouter, Depends, HTTPException
import sqlite3

from services import user_service

from schemas import Usuario, UserUpdate, UsuarioResponse, MessageResponse
from services.auth_service import register_user
from dependencies import get_current_user
from auth import hash_password
from database import get_db
from exceptions import UserAlreadyExistsError, UserNotFoundError

router = APIRouter()

#PERFIL/ruta protegida
@router.get("/profile")
def profile(usuario = Depends(get_current_user)):

    return usuario 

#BUSCA TODOS LOS USUARIOS
@router.get("/users",response_model=list[UsuarioResponse])
def get_users(
    db: sqlite3.Connection = Depends(get_db)
):
    return user_service.get_all_users(db)

#BUSCAR POR ID
@router.get("/users/{user_id}",response_model=UsuarioResponse)
def get_user_by_id(
    user_id: int,
    db: sqlite3.Connection = Depends(get_db)
):
    try:
        return user_service.get_user_by_id(db, user_id)

    except UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
#MODIFICA USUARIO POR ID
@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    datos: UserUpdate,
    db: sqlite3.Connection = Depends(get_db)
):
    try:
        user_service.update_user(
            db=db,
            user_id=user_id,
            nombre=datos.nombre,
            email=datos.email
        )

        return {
            "message": "Usuario actualizado correctamente"
        }

    except UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

#BORRA USUARIO
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: sqlite3.Connection = Depends(get_db)
):
    try:
        user_service.delete_user(
            db=db,
            user_id=user_id
        )

        return {
            "message": "Usuario eliminado correctamente"
        }

    except UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )



#REGISTRO
@router.post("/register",response_model=MessageResponse)#va a routes/users y despues la logica de negocio a servicios
def register(usuario: Usuario,db: sqlite3.Connection = Depends(get_db)):
    password_hash = hash_password(usuario.password)

    try:

        register_user(
            usuario,
            db
        )

        return {
            "mensaje": "Usuario registrado"
        }

    except UserAlreadyExistsError:

        return {
            "mensaje": "El correo electrónico ya está registrado"
        }

#SOLICITUDES
'''{
    "nombre":"Juan",
    "email":"juan@gmail.com",
    "password":"123456"
}'''
