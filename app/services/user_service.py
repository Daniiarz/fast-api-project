from databases.core import Connection
from fastapi import HTTPException, status

import schemas
from repository.user import create_user, check_user_existence
from services.utils import get_password_hash


class UserService:

    @classmethod
    async def create_user(cls, db: Connection, data: schemas.UserRegister):
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
        user_exists = await check_user_existence(db, data.username)
        if user_exists:
            raise credentials_exception
        hashed_password = get_password_hash(data.password)
        user_data = data.dict()
        user_data.pop("password")
        user_data["is_active"] = True
        await create_user(db, user_data, hashed_password)
