from databases.core import Connection
from fastapi import Depends, status, APIRouter

import repository
import schemas
from repository.database.dependencies import get_async_db

router = APIRouter(
    prefix="/items",
    tags=["users"],
)


@router.get("/", response_model=list[schemas.Item], status_code=status.HTTP_200_OK)
async def read_items(skip: int = 0, limit: int = 100, db: Connection = Depends(get_async_db)):
    items = await repository.item.get_async_items(db, skip=skip, limit=limit)
    return items


@router.get("/grouping-set", response_model=list[schemas.ItemGroupingSet], status_code=status.HTTP_200_OK)
async def group_items_by_attrs(db: Connection = Depends(get_async_db)):
    grouping_set = await repository.item.get_async_grouping_set_of_items(db)
    return grouping_set
