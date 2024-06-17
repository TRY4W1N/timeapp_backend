from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.domain.ctx.category.dto import CategoryAddDTO
from src.domain.ctx.category.entity import CategoryEntity
from src.infrastructure.di.alias import UsecaseCategoryAddType, UserEntityType

category_router = APIRouter(route_class=DishkaRoute)


@category_router.post("/")
async def category_add(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryAddType],
    obj: CategoryAddDTO,
) -> CategoryEntity:
    result = await uc.execute(user=user, obj=obj)
    return result
