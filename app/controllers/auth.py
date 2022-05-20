import os
from datetime import timedelta

from databases.core import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from repository.database.dependencies import get_async_db
from schemas.auth import Token
from services.auth.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post("/login", response_model=Token)
async def login(db: Connection = Depends(get_async_db), data: OAuth2PasswordRequestForm = Depends()):
    """
    :param db: async database connection
    :param data: username and password of a user
    :return:
    """
    user = await AuthService.authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expiration_days = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 3))
    access_token_expiration = timedelta(days=expiration_days)
    return AuthService.create_access_token({"sub": str(user.id)}, access_token_expiration)
