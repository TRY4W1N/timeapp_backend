from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.infrastructure.di.alias import MongoClientType
from src.presentation.http.controllers.heal.schemas import HealCheckDatabaseSchema

hs_router = APIRouter(route_class=DishkaRoute)


@hs_router.get("/database")
async def healcheck_database(
    mongo_client: FromDishka[MongoClientType],
) -> HealCheckDatabaseSchema:
    result = await mongo_client.server_info()
    return HealCheckDatabaseSchema(version=result["version"])
