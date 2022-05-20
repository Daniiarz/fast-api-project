from databases.core import Connection
from fastapi import Depends, APIRouter, status

import schemas
from entity.user import User
from repository.database.dependencies import get_async_db
from services.auth.auth_dependecies import get_current_user
from services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserRegister, db: Connection = Depends(get_async_db)):
    await UserService.create_user(db, user)


@router.get("/me", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def get_user_profile(user: User = Depends(get_current_user)):
    return user
