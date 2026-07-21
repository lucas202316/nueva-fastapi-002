from fastapi import APIRouter,Depends
from schemas import Login
from database import  get_db
from auth import (
verify_password,
create_access_token
)
import sqlite3
router = APIRouter()



#LOGIN
@router.post("/login")#va a routes/auth
def login(datos: Login,db: sqlite3.Connection = Depends(get_db)):#ademas de datos debe recibir db de dependens(get_db)
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
            "access_token": token
        }

           
    return {
        "error": "Correo o contraseña incorrectos."
    }
