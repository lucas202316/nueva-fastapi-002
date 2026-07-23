#define qué errores existen (UserNotFoundError, EmailAlreadyExistsError, etc.).


class UserAlreadyExistsError(Exception):
    """Se lanza cuando se intenta registrar un usuario con un email ya existente."""
    pass

class UserNotFoundError(Exception):
    pass #la vamos a usar en  def get_user_by_id() del services

class InvalidCredentialsError(Exception):
    pass

class PermissionDeniedError(Exception):
    """Se lanza cuando un usuario no tiene permisos para realizar una acción."""
    pass
