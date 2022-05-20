import asyncio

from redis.asyncio import Redis  # noqa

from schemas.chat import Message


class ChatRepository:

    @classmethod
    async def write_message_to_room(cls, connection: Redis, message: Message):
        async with connection.pipeline(transaction=True) as pipeline:
            await (
                pipeline
                    .sadd(f"user:{message.sender_id}:rooms", message.room_id)
                    .sadd(f"user:{message.receiver_id}:rooms", message.room_id)
                    .zadd(message.room_id, {message.json(): message.timestamp})
                    .execute()
            )

    @classmethod
    async def create_private_room(cls, connection: Redis, user_id: int, receiver_id: int, room_id: str):
        async with connection.pipeline(transaction=True) as pipeline:
            await (
                pipeline
                    .sadd(f"user:{user_id}:rooms", room_id)
                    .sadd(f"user:{receiver_id}:rooms", room_id)
                    .execute()
            )

    @classmethod
    async def get_room_messages(
            cls,
            connection: Redis,
            user_id: int,
            room_id: str,
            offset: int,
            limit: int,
    ) -> list[Message] | None:
        user_room: int = await connection.exists(f"user:{user_id}:rooms", f"{room_id}")
        if not user_room:
            return None
        messages: str = await connection.zrange(name=room_id, start=offset, end=limit + offset, desc=True)
        return [Message.parse_raw(i) for i in messages]

    @classmethod
    async def get_user_rooms(cls, connection: Redis, user_id: int):
        user_rooms = await connection.smembers(f"user:{user_id}:rooms")
        last_messages = await asyncio.gather(
            *[connection.zrange]
        )
