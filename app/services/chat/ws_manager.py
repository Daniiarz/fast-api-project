from typing import Dict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: int):
        conn = self.active_connections.pop(user_id)
        await conn.close()

    async def send_personal_message(self, receiver_id: int, message: str):
        if receiver_id not in self.active_connections:
            return
        await self.active_connections[receiver_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)
