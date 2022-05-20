from redis.asyncio.client import Redis  # noqa

from repository.chat import ChatRepository
from schemas.chat import Message


class WebSocketService:

    @staticmethod
    def get_room_id(user_id: int, receiver_id: int) -> str:
        return f"{min(user_id, receiver_id)}:{max(user_id, receiver_id)}"

    @classmethod
    async def add_message_to_room(cls, connection: Redis, message: Message):
        await ChatRepository.write_message_to_room(connection, message)
