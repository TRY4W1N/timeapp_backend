from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

user_router = APIRouter(route_class=DishkaRoute)
