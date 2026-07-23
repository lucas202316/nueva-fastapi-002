from fastapi import APIRouter,Depends
from schemas import Login, Token
from database import  get_db
from auth import (
verify_password,
create_access_token
)
import sqlite3
router = APIRouter()
from services import auth_service
from fastapi.security import OAuth2PasswordRequestForm



#LOGIN
@router.post("/login",response_model=Token)#va a routes/auth
def login(datos: OAuth2PasswordRequestForm = Depends(),db: sqlite3.Connection = Depends(get_db)):#ademas de datos debe recibir db de dependens(get_db)
    

    return auth_service.login(
    db,
    datos.username,
    datos.password
)

    
    
    
