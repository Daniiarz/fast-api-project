import asyncio

from fastapi import WebSocket, Depends
from pydantic import ValidationError
from redis.asyncio.client import Redis  # noqa

from entity.user import User
from repository.database.dependencies import get_redis_db
from schemas.chat import Message
from services.auth.auth_dependecies import get_current_user
from services.chat.ws_manager import ConnectionManager
from services.chat.ws_service import WebSocketService

CONNECTION_MANAGER = ConnectionManager()


async def websocket_connection(
        websocket: WebSocket,
        user: User = Depends(get_current_user),
        redis: Redis = Depends(get_redis_db)
):
    await CONNECTION_MANAGER.connect(user_id=user.id, websocket=websocket)
    async for data in websocket.iter_text():
        try:
            message = Message.parse_raw(data)
        except ValidationError as e:
            continue

        message.room_id = WebSocketService.get_room_id(user.id, message.receiver_id)
        message.sender_id = user.id
        await asyncio.gather(
            CONNECTION_MANAGER.send_personal_message(receiver_id=message.receiver_id, message=message.json()),
            WebSocketService.add_message_to_room(connection=redis, message=message)
        )
