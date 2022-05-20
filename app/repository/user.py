from databases.core import Connection
from sqlalchemy import select, insert

from entity.user import User


async def get_user(db: Connection, user_id: int):
    query = select(User).filter(User.id == user_id)
    user_data = await db.fetch_one(query)
    return User(**user_data)


async def get_user_by_username(db: Connection, username: str):
    query = select(User).where(User.username == username)
    result = await db.fetch_one(query)
    user = User(**result)
    return user


async def check_user_existence(db: Connection, username: str) -> bool:
    query = select(select(User.username).where(User.username == username).exists())
    user_existence = await db.execute(query)
    return user_existence


async def create_user(db: Connection, user_data: dict, hashed_password: str):
    async with db.transaction():
        query = (
            insert(User)
                .values(**user_data, hashed_password=hashed_password)
                .returning(User.id, User.first_name, User.last_name, User.username)
        )
        result = await db.execute(query)
    return result
