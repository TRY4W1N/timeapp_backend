from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.domain.ctx.user.entity import UserEntity
from src.infrastructure.di.alias import UserEntityType

user_router = APIRouter(route_class=DishkaRoute)

@user_router.get("/current")
async def get_current_user(
    user: FromDishka[UserEntityType],
) -> UserEntity:
    return user