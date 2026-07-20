from database import conexion,cursor
from fastapi import FastAPI, Depends, HTTPException, status
from schemas import Usuario,Login
import bcrypt
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)
import sqlite3
#extrae automáticamente el token Bearer del encabezado Authorization
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


app = FastAPI()








#FUNCIONES AUXILIARES
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        user_id = payload.get("id")


        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )


        return {"id": user_id}


    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el token"
        )



#ENDPOINTS
#INICIO
@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}

#LOGIN
@app.post("/login")
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

#PERFIL/ruta protegida
@app.get("/profile")
def profile(usuario = Depends(get_current_user)):

    return usuario 




#REGISTRO
@app.post("/register")
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
