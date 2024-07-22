from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from fastapi import APIRouter

from src.infrastructure.di.alias import UseCaseGetCategoryStatisticType, UserEntityType
from src.presentation.http.controllers.statistic.schemas import (
    ListCategoryTimeStatisticSchema,
)
from src.presentation.http.common.responses import response_404

statistic_router = APIRouter(route_class=DishkaRoute)


@statistic_router.get("/category/time_total", responses={**response_404})
async def get_statistic_category_time_total(
    user: FromDishka[UserEntityType], uc: FromDishka[UseCaseGetCategoryStatisticType]
) -> ListCategoryTimeStatisticSchema:
    res = await uc.execute(user=user)
    return ListCategoryTimeStatisticSchema.from_obj(obj_list=res)
