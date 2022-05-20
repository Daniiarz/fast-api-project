import os

from databases.core import Connection
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from common.base_classes import OAuth2PasswordBearerHeader
from entity.user import User
from repository.database.dependencies import get_async_db
from repository.user import get_user
from schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearerHeader(tokenUrl="/authentication/login")


async def get_current_user(db: Connection = Depends(get_async_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        user_id: str = payload.get("sub")
        if user_id is None or not user_id.isnumeric():
            raise credentials_exception
        token_data = TokenData(id=int(user_id))
    except JWTError:
        raise credentials_exception
    user = await get_user(db, token_data.id)
    if user is None:
        raise credentials_exception
    return user
