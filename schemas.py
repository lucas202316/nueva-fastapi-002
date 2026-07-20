from pydantic import BaseModel

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