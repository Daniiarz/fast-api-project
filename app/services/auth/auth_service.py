import datetime
import os
from datetime import timedelta

from databases.core import Connection
from jose import jwt
from passlib.context import CryptContext

from entity.user import User
from repository.user import get_user_by_username

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def authenticate_user(cls, db: Connection, username: str, password: str) -> bool | User:
        user = await get_user_by_username(db, username)
        if not user:
            return False
        if not cls._verify_password(password, user.hashed_password):
            return False
        return user

    @classmethod
    def create_access_token(cls, data: dict, expiration_delta: timedelta) -> dict:
        encode_data = data.copy()
        expiration_datetime = datetime.datetime.now() + expiration_delta
        encode_data.update({"exp": expiration_datetime})
        encoded_jwt = jwt.encode(encode_data, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
        return {"access_token": encoded_jwt, "token_type": "bearer"}
