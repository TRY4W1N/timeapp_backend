from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException
from pymongo.errors import ServerSelectionTimeoutError

from src.infrastructure.di.alias import MongoClientType

hs_router = APIRouter(route_class=DishkaRoute)


@hs_router.get("/")
async def healcheck_database(
    mongo_client: FromDishka[MongoClientType],
) -> dict:
    try:
        result = await mongo_client.server_info()
    except ServerSelectionTimeoutError as e:
        raise HTTPException(
            status_code=500, detail=dict(msg="Database is unavailable", status=False, version=None)
        ) from e
    return dict(detail=dict(msg="ok", version=result["version"], status=bool(result["ok"])))
