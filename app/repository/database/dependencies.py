from repository.database.async_postgres import database
from repository.database.postgres import SessionFactory
from repository.database.redis import connection


def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    return database


async def get_redis_db():
    return connection
