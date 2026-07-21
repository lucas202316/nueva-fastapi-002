from fastapi import APIRouter, Depends, status
import sqlite3
from schemas import Usuario, UserUpdate, UsuarioResponse,MessageResponse
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
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(
    usuario: Usuario,
    db: sqlite3.Connection = Depends(get_db)
):

   

        register_user(
            usuario,
            db
        )

        return {
            "mensaje": "Usuario registrado"
        }

   
#USUARIOS
@router.get("/users",response_model=list[UsuarioResponse])
def get_users(
    db: sqlite3.Connection = Depends(get_db)
):
    return user_service.get_all_users(db)

#BUSCA USUARIOS POR ID
@router.get("/users/{user_id}",response_model=UsuarioResponse)
def get_user_by_id(
    user_id: int,
    db: sqlite3.Connection = Depends(get_db)
):
    
        return user_service.get_user_by_id( 
            db=db,
            user_id=user_id
            )

    
#ACTUALIZA POR ID
@router.put("/users/{user_id}",response_model=UsuarioResponse)
def update_user(
    user_id: int,
    datos: UserUpdate,
    db: sqlite3.Connection = Depends(get_db)
):
    
        return user_service.update_user(
                db=db,
                user_id=user_id,
                nombre=datos.nombre,
                email=datos.email
            )
    
    

#BORRAR USUARIO
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: sqlite3.Connection = Depends(get_db)
):
   
        user_service.delete_user(
            db=db,
            user_id=user_id
        )

       

    
