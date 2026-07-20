from fastapi import Depends, HTTPException, status
from auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

#extrae automáticamente el token Bearer del encabezado Authorization
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

#FUNCIONES AUXILIARES
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)


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
