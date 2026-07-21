from pydantic import BaseModel
#modelos de datos pydantic



class Usuario(BaseModel):
    nombre: str
    email: str
    password: str
    
class Login(BaseModel):
   email: str
   password: str

class UserUpdate(BaseModel):
    nombre: str
    email: str
