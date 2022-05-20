from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from repository.database.postgres import BaseModel


class Item(BaseModel):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("entity.user.User", back_populates="items")
