from fastapi import APIRouter, Depends
import sqlite3
from schemas import Usuario
from database import get_db
from dependencies import get_current_user
from exceptions import UserAlreadyExistsError
from services import user_service
from services.auth_service import register_user
router = APIRouter()

'''
Todos los endpoints recibirán la conexión mediante:
db: sqlite3.Connection = Depends(get_db)
Y dentro del endpoint crearán su propio cursor:
cursor = db.cursor()

'''



#PERFIL/ruta protegida
@router.get("/profile")
def profile(usuario = Depends(get_current_user)):

    return usuario 

#REGISTRO
@router.post("/register")
def register(usuario: Usuario, db: sqlite3.Connection = Depends(get_db)):
    
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

#USUARIOS
@router.get("/users")
def get_users(
    db: sqlite3.Connection = Depends(get_db)
):
    return user_service.get_all_users(db)

