
from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.users import router as users_router
from handlers import (
                        user_not_found_handler, 
                        user_already_exists_handler, 
                        invalid_credentials_handler,
                        permission_denied_handler)
from exceptions import (
                        UserNotFoundError, 
                        UserAlreadyExistsError, 
                        InvalidCredentialsError,
                        PermissionDeniedError)



app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)

app.add_exception_handler(
    UserNotFoundError,
    user_not_found_handler
)
app.add_exception_handler(
    UserAlreadyExistsError,
    user_already_exists_handler
)
app.add_exception_handler(
    InvalidCredentialsError,
    invalid_credentials_handler
)

app.add_exception_handler(
    PermissionDeniedError,
    permission_denied_handler
)


#ENDPOINTS
#INICIO
@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}





