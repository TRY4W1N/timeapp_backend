from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader

from src.presentation.http.controllers.category.controller import category_router
from src.presentation.http.controllers.heal.controller import hs_router
from src.presentation.http.controllers.interval.controller import interval_router
from src.presentation.http.controllers.user.controller import user_router

router = APIRouter(route_class=DishkaRoute)

router.include_router(
    prefix="/heal",
    tags=["Heal"],
    router=hs_router,
)

router.include_router(
    prefix="/user",
    tags=["User"],
    router=user_router,
    dependencies=[Depends(APIKeyHeader(name="Authorization", scheme_name="Authorization", auto_error=True))],
)
router.include_router(
    prefix="/category",
    tags=["Category"],
    router=category_router,
    dependencies=[Depends(APIKeyHeader(name="Authorization", scheme_name="Authorization", auto_error=True))],
)
router.include_router(
    prefix="/interval",
    tags=["Interval"],
    router=interval_router,
    dependencies=[Depends(APIKeyHeader(name="Authorization", scheme_name="Authorization", auto_error=True))],
)
