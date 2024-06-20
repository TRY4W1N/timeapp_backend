from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import (
    IntervalClearDTO,
    IntervalStartDTO,
    IntervalStopDTO,
)
from src.infrastructure.di.alias import (
    UsecaseIntervalClearType,
    UsecaseIntervalTrackStartType,
    UsecaseIntervalTrackStopType,
    UserEntityType,
)

interval_router = APIRouter(route_class=DishkaRoute)


@interval_router.post("/start/{category_uuid}")
async def interval_track_start(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseIntervalTrackStartType],
    category_uuid: CategoryId,
) -> IntervalStartDTO:
    result = await uc.execute(user=user, category_uuid=category_uuid)
    return result


@interval_router.post("/stop/{category_uuid}")
async def interval_track_stop(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseIntervalTrackStopType],
    category_uuid: CategoryId,
) -> IntervalStopDTO:
    result = await uc.execute(user=user, category_uuid=category_uuid)
    return result


@interval_router.delete("/clear/{category_uuid}")
async def interval_clear_by_category(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseIntervalClearType],
    category_uuid: CategoryId,
) -> IntervalClearDTO:
    result = await uc.execute(user=user, category_uuid=category_uuid)
    return result
