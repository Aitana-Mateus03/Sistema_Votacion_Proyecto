
from api.auth.security import hash_password

# Usuarios de prueba para demostrar autenticación y roles.
# En producción, estos usuarios deben almacenarse en una base de datos.

USERS_DB = {
    "admin": {
        "username": "admin",
        "password": hash_password("Admin123*"),
        "role": "ADMIN"
    },
    "usuario": {
        "username": "usuario",
        "password": hash_password("Usuario123*"),
        "role": "USER"
    }
}


def get_user(username: str):
    return USERS_DB.get(username)
