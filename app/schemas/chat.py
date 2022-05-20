import time

from pydantic import BaseModel, Field


class BaseMessage(BaseModel):
    sender_id: int
    receiver_id: int
    message: str


class Message(BaseMessage):
    timestamp: float | None = Field(default_factory=time.time)
    room_id: str | None = None
    is_read: bool | None = False
