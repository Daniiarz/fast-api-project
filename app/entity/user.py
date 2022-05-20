from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from repository.database.postgres import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)

    hashed_password = Column(String)

    is_active = Column(Boolean, nullable=False, default=True)
    items = relationship("entity.item.Item", back_populates="owner")
