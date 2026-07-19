import sqlite3
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
import bcrypt
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


app = FastAPI()

#CONSTANTES
SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"



#MODELOS
#REGISTRO
class Usuario(BaseModel):
   nombre: str
   email: str
   password: str

#LOGIN   
class Login(BaseModel):
   email: str
   password: str


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
    if bcrypt.checkpw(
        datos.password.encode(),
        password_guardada.encode()
    ):
           
        token = jwt.encode(
        {"id": usuario[0]},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
       
        return {
            "access_token": token
        }

           
    return {
        "error": "Correo o contraseña incorrectos."
    }

#PERFIL
@app.get("/profile")
def profile(usuario = Depends(get_current_user)):

    return usuario


#conexión a la base de datos
ruta = r"C:\Lucas\bbdd\mi_api.db"
conexion = sqlite3.connect(
    ruta,
    check_same_thread=False
)
cursor = conexion.cursor()

#REGISTRO
@app.post("/register")
def register(usuario: Usuario):
    hash_password = bcrypt.hashpw(
        usuario.password.encode(),
        bcrypt.gensalt()
    )
    try:
        cursor.execute(
            """
            INSERT INTO usuarios(nombre, email, password)
            VALUES (?, ?, ?)
            """,
            (
                usuario.nombre,
                usuario.email,
                hash_password.decode() #porque estaba en bytes y hay que pasarlo a texto
            )
        )
        conexion.commit()

    except sqlite3.IntegrityError:
        return {"mensaje": "El correo electrónico ya está registrado"}
    
    return {
            "mensaje": "Usuario registrado",
            "password_original": usuario.password,
            "password_hasheada": hash_password.decode()

        }


#SOLICITUDES
'''{
    "nombre":"Juan",
    "email":"juan@gmail.com",
    "password":"123456"
}'''
