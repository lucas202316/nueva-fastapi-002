import bcrypt
from jose import jwt

from config import SECRET_KEY, ALGORITHM







def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()




def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        password_hash.encode()
    )




def create_access_token(user_id: int) -> str:
    return jwt.encode(
        {"id": user_id},
        SECRET_KEY,
        algorithm=ALGORITHM
    )




def decode_access_token(token: str):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
