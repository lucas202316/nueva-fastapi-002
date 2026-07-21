import sqlite3
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
import bcrypt
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer#

#extrae automáticamente el token Bearer del encabezado Authorization
#va en dependencies.py
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


app = FastAPI()

#CONSTANTES va a config.py
SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"

#conexión a la base de datos
ruta = r"C:\Lucas\bbdd\mi_api.db"#va a config.py
conexion = sqlite3.connect(
    ruta,
    check_same_thread=False
)
cursor = conexion.cursor()#cursor global debe pasar a funcion en database.py

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


#FUNCIONES AUXILIARES va para dependencies.py
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(#para verificar token
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
@app.post("/login")#va a routes/auth
def login(datos: Login):#ademas de datos debe recibir db de dependens(get_db)
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
    if bcrypt.checkpw(#verifica contraseña
        datos.password.encode(),
        password_guardada.encode()
    ):
           
        token = jwt.encode(#genera token
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

#PERFIL/ruta protegida
@app.get("/profile")
def profile(usuario = Depends(get_current_user)):

    return usuario 




#REGISTRO
@app.post("/register")#va a routes/users y despues la logica de negocio a servicios
def register(usuario: Usuario):
    hash_password = bcrypt.hashpw(#creacion del hash
        usuario.password.encode(),
        bcrypt.gensalt()
    )
    try:
        cursor.execute(#logica de acceso a datos debe ir en /user_repositories.py
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

    except sqlite3.IntegrityError:#en el services no debe depender de sqlite q una capa inferior
        #debemos crear nuestras propias excepciones, propias de la aplicacion: exceptions.py
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
