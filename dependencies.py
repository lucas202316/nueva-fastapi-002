from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from services.user_service import is_admin
from exceptions import PermissionDeniedError


from auth import (
    decode_access_token
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

def require_role(required_role: str):
    def role_checker(
        current_user=Depends(get_current_user)
    ):

        if current_user["rol"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción"
            )

        return current_user

    return role_checker



def get_current_user(token: str = Depends(oauth2_scheme)):
    try:


        payload = decode_access_token(token)

        user_id = int(payload.get("sub"))
        rol = payload.get("rol")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )


        return {"id": user_id,
                "rol": rol}


    except JWTError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el token"
        )

def require_admin(
    usuario: dict = Depends(get_current_user)
):
    if not is_admin(usuario):
        raise PermissionDeniedError
    return usuario
