from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from src.domain.ctx.category.dto import (
    CategoryCreateDTO,
    CategoryFilterDTO,
    CategoryUpdateDTO,
)
from src.domain.ctx.category.entity import CategoryEntity
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import (
    IntervalClearDTO,
    IntervalStartDTO,
    IntervalStopDTO,
)
from src.infrastructure.di.alias import (
    UsecaseCategoryClearType,
    UsecaseCategoryCreateType,
    UsecaseCategoryDeleteType,
    UsecaseCategoryGetListType,
    UsecaseCategoryTrackStartType,
    UsecaseCategoryTrackStopType,
    UsecaseCategoryUpdateType,
    UserEntityType,
)

category_router = APIRouter(route_class=DishkaRoute)


@category_router.get("/")
async def category_list(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryGetListType],
    obj: CategoryFilterDTO = Depends(),
) -> list[CategoryEntity]:
    result = await uc.execute(user=user, obj=obj)
    return result


@category_router.post("/")
async def category_create(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryCreateType],
    obj: CategoryCreateDTO,
) -> CategoryEntity:
    result = await uc.execute(user=user, obj=obj)
    return result


@category_router.patch("/{uuid}")
async def category_update(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryUpdateType],
    uuid: CategoryId,
    obj: CategoryUpdateDTO,
) -> CategoryEntity:
    result = await uc.execute(user=user, category_uuid=uuid, obj=obj)
    return result


@category_router.delete("/clear/{uuid}")
async def category_clear(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryClearType],
    uuid: CategoryId,
) -> IntervalClearDTO:
    result = await uc.execute(user=user, category_uuid=uuid)
    return result


@category_router.delete("/delete/{uuid}")
async def category_delete(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryDeleteType],
    uuid: CategoryId,
) -> CategoryId:
    result = await uc.execute(user=user, category_uuid=uuid)
    return result


@category_router.post("/track/start/{uuid}")
async def category_track_start(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryTrackStartType],
    uuid: CategoryId,
) -> IntervalStartDTO:
    result = await uc.execute(user=user, category_uuid=uuid)
    return result


@category_router.post("/track/stop/{uuid}")
async def category_track_stop(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryTrackStopType],
    uuid: CategoryId,
) -> IntervalStopDTO:
    result = await uc.execute(user=user, category_uuid=uuid)
    return result
