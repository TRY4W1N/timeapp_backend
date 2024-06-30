from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from src.domain.ctx.category.interface.types import CategoryId
from src.infrastructure.di.alias import (
    UsecaseCategoryCreateType,
    UsecaseCategoryDeleteType,
    UsecaseCategoryGetListType,
    UsecaseCategoryUpdateType,
    UserEntityType,
)
from src.presentation.http.controllers.category.schemas import (
    CategoryCreateSchema,
    CategoryDeleteSchema,
    CategoryFilterSchema,
    CategorySchema,
    CategoryUpdateSchema,
    CategorySListSchema,
)

category_router = APIRouter(route_class=DishkaRoute)


@category_router.get("/")
async def category_list(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryGetListType],
    obj: CategoryFilterSchema = Depends(),
) -> CategorySListSchema:
    filter_obj = obj.to_obj()
    result = await uc.execute(user=user, obj=filter_obj)
    return CategorySListSchema.from_obj(category_list=result)


@category_router.post("/")
async def category_create(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryCreateType],
    in_obj: CategoryCreateSchema,
) -> CategorySchema:
    obj = in_obj.to_obj()
    result = await uc.execute(user=user, obj=obj)
    return CategorySchema.from_obj(category_obj=result)


@category_router.patch("/{uuid}")
async def category_update(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryUpdateType],
    uuid: CategoryId,
    in_obj: CategoryUpdateSchema,
) -> CategorySchema:
    obj = in_obj.to_obj()
    result = await uc.execute(user=user, category_uuid=uuid, obj=obj)
    return CategorySchema.from_obj(category_obj=result)


@category_router.delete("/delete/{uuid}")
async def category_delete(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryDeleteType],
    uuid: CategoryId,
) -> CategoryDeleteSchema:
    result = await uc.execute(user=user, category_uuid=uuid)
    return CategoryDeleteSchema.from_obj(category_obj=result)
