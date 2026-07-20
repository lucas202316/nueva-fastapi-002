from fastapi import APIRouter
from fastapi import APIRouter
from schemas import Login
from database import cursor
from auth import (
verify_password,
create_access_token
)


router = APIRouter()

#LOGIN
@router.post("/login")
def login(datos: Login):
    cursor.execute(
            "SELECT * FROM usuarios WHERE email = ?",
            (datos.email,)
        )


    usuario = cursor.fetchone()
    if usuario is None:
            return {
                "error": "Correo o contraseña incorrectos."
            }
    password_guardada = usuario[3]
    if verify_password(
        datos.password,
        password_guardada
):

           
        token = create_access_token(usuario[0])
       
        return {
            "access_token": token
        }

           
    return {
        "error": "Correo o contraseña incorrectos."
    }

