from fastapi import APIRouter, Depends
from schemas import Login, Token
from database import get_db
import sqlite3
from auth import (
verify_password,
create_access_token
)


router = APIRouter()

'''
Todos los endpoints recibirán la conexión mediante:
db: sqlite3.Connection = Depends(get_db)
Y dentro del endpoint crearán su propio cursor:
cursor = db.cursor()

'''


#LOGIN
@router.post("/login",response_model=Token)
def login(datos: Login, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
            "SELECT * FROM usuarios WHERE email = ?",
            (datos.email,)
        )


    usuario = cursor.fetchone()
    if usuario is None:
            return {
                "error": "Correo o contraseña incorrectos."
            }
    password_guardada = usuario["password"]
    if verify_password(
        datos.password,
        password_guardada
):

           
        token = create_access_token(usuario["id"])
       
        return {
            "access_token": token,
            "token_type": "bearer"
        }

           
    return {
        "error": "Correo o contraseña incorrectos."
    }

