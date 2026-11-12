
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.auth.security import verify_password, create_access_token
from api.auth.users import get_user
from api.auth.dependencies import get_current_user, require_role

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)

    if not user or not verify_password(
        form_data.password, user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )

    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user["role"]
    }


@router.get("/admin")
def admin_endpoint(
    current_user: dict = Depends(require_role("ADMIN"))
):
    return {
        "message": "Acceso autorizado para ADMIN",
        "user": current_user["username"],
        "role": current_user["role"]
    }


@router.get("/user")
def user_endpoint(
    current_user: dict = Depends(require_role("USER"))
):
    return {
        "message": "Acceso autorizado para USER",
        "user": current_user["username"],
        "role": current_user["role"]
    }
