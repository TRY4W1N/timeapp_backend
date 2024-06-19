from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.presentation.http.controllers.category.controller import category_router
from src.presentation.http.controllers.user.controller import user_router
from src.presentation.http.controllers.interval.controller import interval_router

router = APIRouter(route_class=DishkaRoute)
router.include_router(
    prefix="/user",
    tags=["User"],
    router=user_router,
)
router.include_router(
    prefix="/category",
    tags=["Category"],
    router=category_router,
)
router.include_router(
    prefix="/interval",
    tags=["Interval"],
    router=interval_router,
)
