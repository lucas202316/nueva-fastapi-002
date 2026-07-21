from pydantic import BaseModel

#MODELOS
#BASE
class UsuarioBase(BaseModel):
    nombre: str
    email: str



#REGISTRO
class Usuario(UsuarioBase):
   password: str

#LOGIN   
class Login(BaseModel):
   email: str
   password: str
   
#ACTUALIZACIONES
class UserUpdate(UsuarioBase):
    pass

#MODELOS DE RESPUESTAS
class UsuarioResponse(UsuarioBase):
    id: int

#RESPUESTA DEL LOGIN --> Para documentar correctamente el endpoint de login.
class Token(BaseModel):
    access_token: str
    token_type: str

#RESPUESTA DEL REGISTRO
class MessageResponse(BaseModel):
    mensaje: str
