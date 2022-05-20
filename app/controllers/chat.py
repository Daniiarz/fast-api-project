from fastapi import APIRouter, Depends, status
from redis.asyncio.client import Redis  # noqa

from entity.user import User
from repository.database.dependencies import get_redis_db
from schemas.chat import Message
from services.auth.auth_dependecies import get_current_user
from services.chat.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("/rooms/{user_id}")
async def get_user_rooms(user: User = Depends(get_current_user)):
    pass


@router.get("/rooms/{room_id}/messages", response_model=list[Message], status_code=status.HTTP_200_OK)
async def get_room_messages(
        room_id: str,
        offset: int = 0,
        limit: int = 100,
        db: Redis = Depends(get_redis_db),
        user: User = Depends(get_current_user)
):
    return await ChatService.get_room_messages(connection=db, user=user, room_id=room_id, limit=limit, offset=offset)
