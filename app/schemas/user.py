from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str


class UserRegister(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    # items: list[Item] = []

    class Config:
        orm_mode = True
