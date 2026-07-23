#define cómo esos errorres de exceptions.py  se convierten en respuestas HTTP (404, 409, etc.).

from fastapi import Request, status
from fastapi.responses import JSONResponse
from exceptions import( UserNotFoundError, 
                        UserAlreadyExistsError, 
                        InvalidCredentialsError, 
                        PermissionDeniedError
)

def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Usuario no encontrado"
        }
    )

def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "El correo electrónico ya está registrado"
        }
    )

def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Correo o contraseña incorrectos."
        }
    )

def permission_denied_handler(
    request: Request,
    exc: PermissionDeniedError
):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail": "No tienes permisos para realizar esta acción."
        }
    )
