#las funciones para crear y verificar el hash
#las funciones para crear y decodificar el JWT
import bcrypt
from jose import jwt
from config import SECRET_KEY, ALGORITHM
#CONSTANTES

#funcion crear hash
def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

#funcion para verificar el hash
def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        password_hash.encode()
    )

#funcion crear JWT
def create_access_token(user_id: int) -> str:
    return jwt.encode(
        {"id": user_id},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

#funcion verifica token
def decode_access_token(token: str):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
