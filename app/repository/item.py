from databases.core import Connection
from sqlalchemy import tuple_
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from sqlalchemy.sql.functions import grouping_sets

import entity.item as entity
import schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(entity.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, data: schemas.ItemCreate, user_id: int):
    db_entity = entity.Item(**data.dict(), owner_id=user_id)
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity


def get_grouping_set_of_items(db: Session):
    groping_set = db.query(entity.Item.title, entity.Item.description).group_by(
        grouping_sets(
            tuple_(entity.Item.description, ),
            tuple_(entity.Item.title, )
        )
    ).all()
    return groping_set


async def get_async_items(db: Connection, skip: int = 0, limit: int = 100):
    query = select(entity.Item).offset(skip).limit(limit)
    return await db.fetch_all(query)


async def get_async_grouping_set_of_items(db: Connection):
    grouping_set = select(entity.Item.title, entity.Item.description).group_by(
        grouping_sets(
            tuple_(entity.Item.description),
            tuple_(entity.Item.title),
        )
    )
    return await db.execute(grouping_set)


class ItemRepository:

    @staticmethod
    async def get_async_items(db: Connection, skip: int = 0, limit: int = 100):
        query = select(entity.Item).offset(skip).limit(limit)
        return await db.fetch_all(query)

    @staticmethod
    async def get_async_grouping_set_of_items(db: Connection):
        grouping_set = select(entity.Item.title, entity.Item.description).group_by(
            grouping_sets(
                tuple_(entity.Item.description),
                tuple_(entity.Item.title),
            )
        )
        return await db.execute(grouping_set)
