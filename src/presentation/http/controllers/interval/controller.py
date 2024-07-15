from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.domain.ctx.category.interface.types import CategoryId
from src.infrastructure.di.alias import (
    UsecaseIntervalClearType,
    UsecaseIntervalTrackStartType,
    UsecaseIntervalTrackStopType,
    UserEntityType,
)
from src.presentation.http.common.responses import (
    response_400_not_created,
    response_404,
)
from src.presentation.http.controllers.interval.schemas import (
    IntervalClearSchema,
    IntervalStartSchema,
    IntervalStopSchema,
)

interval_router = APIRouter(route_class=DishkaRoute)


@interval_router.post("/start/{category_uuid}", responses={**response_400_not_created, **response_404})
async def interval_track_start(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseIntervalTrackStartType],
    category_uuid: CategoryId,
) -> IntervalStartSchema:
    result = await uc.execute(user=user, category_uuid=category_uuid)
    return IntervalStartSchema.from_obj(obj=result)


@interval_router.patch("/stop/{category_uuid}", responses={**response_404})
async def interval_track_stop(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseIntervalTrackStopType],
    category_uuid: CategoryId,
) -> IntervalStopSchema:
    result = await uc.execute(user=user, category_uuid=category_uuid)
    return IntervalStopSchema.from_obj(obj=result)


@interval_router.delete("/clear/{category_uuid}", responses={**response_404})
async def interval_clear_by_category(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseIntervalClearType],
    category_uuid: CategoryId,
) -> IntervalClearSchema:
    result = await uc.execute(user=user, category_uuid=category_uuid)
    return IntervalClearSchema.from_obj(obj=result)
