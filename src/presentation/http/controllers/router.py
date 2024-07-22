from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.presentation.http.common.responses import (
    auth_dependencies,
    response_401,
    response_500,
)
from src.presentation.http.controllers.category.controller import category_router
from src.presentation.http.controllers.heal.controller import hs_router
from src.presentation.http.controllers.interval.controller import interval_router
from src.presentation.http.controllers.user.controller import user_router
from src.presentation.http.controllers.statistic.controller import statistic_router

router = APIRouter(route_class=DishkaRoute, responses={**response_500})

router.include_router(
    prefix="/heal",
    tags=["Heal"],
    router=hs_router,
)

router.include_router(
    prefix="/user",
    tags=["User"],
    router=user_router,
    dependencies=[*auth_dependencies],
    responses={**response_401},
)
router.include_router(
    prefix="/category",
    tags=["Category"],
    router=category_router,
    dependencies=[*auth_dependencies],
    responses={**response_401},
)
router.include_router(
    prefix="/interval",
    tags=["Interval"],
    router=interval_router,
    dependencies=[*auth_dependencies],
    responses={**response_401},
)
router.include_router(
    prefix="/statistic",
    tags=["Statistic"],
    router=statistic_router,
    dependencies=[*auth_dependencies],
    responses={**response_401},
)
