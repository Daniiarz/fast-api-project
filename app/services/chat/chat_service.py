from redis.asyncio.client import Redis  # noqa

from entity.user import User
from repository.chat import ChatRepository


class ChatService:

    @classmethod
    async def get_room_messages(cls, connection: Redis, user: User, room_id: str, limit: int, offset: int):
        messages = await ChatRepository.get_room_messages(
            connection=connection,
            user_id=user.id,
            room_id=room_id,
            limit=limit,
            offset=offset
        )
        return messages
