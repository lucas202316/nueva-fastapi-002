from pydantic import BaseModel
#modelos de datos pydantic
class UsuarioBase(BaseModel):
    nombre: str
    email: str

class Usuario(UsuarioBase):
    password: str
    
class Login(BaseModel):
   email: str
   password: str

class UserUpdate(UsuarioBase):
   pass

class UsuarioResponse(UsuarioBase):
    id: int
    rol: str
    

class Token(BaseModel):
    access_token: str
    token_type: str

class MessageResponse(BaseModel):
    mensaje: str
