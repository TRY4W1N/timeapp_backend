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
from src.presentation.http.common.responses import (
    response_400_not_created,
    response_404,
)
from src.presentation.http.controllers.category.schemas import (
    CategoryCreateSchema,
    CategoryDeleteSchema,
    CategoryFilterSchema,
    CategoryListSchema,
    CategorySchema,
    CategoryUpdateSchema,
)

category_router = APIRouter(route_class=DishkaRoute)


@category_router.get("/")
async def category_list(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryGetListType],
    obj: CategoryFilterSchema = Depends(),
) -> CategoryListSchema:
    filter_obj = obj.to_obj()
    result = await uc.execute(user=user, obj=filter_obj)
    return CategoryListSchema.from_obj(obj_list=result)


@category_router.post("/", responses={**response_400_not_created})
async def category_create(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryCreateType],
    in_obj: CategoryCreateSchema,
) -> CategorySchema:
    obj = in_obj.to_obj()
    result = await uc.execute(user=user, obj=obj)
    return CategorySchema.from_obj(obj=result)


@category_router.patch("/{uuid}", responses={**response_404})
async def category_update(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryUpdateType],
    uuid: CategoryId,
    in_obj: CategoryUpdateSchema,
) -> CategorySchema:
    obj = in_obj.to_obj()
    result = await uc.execute(user=user, category_uuid=uuid, obj=obj)
    return CategorySchema.from_obj(obj=result)


@category_router.delete("/{uuid}", responses={**response_404})
async def category_delete(
    user: FromDishka[UserEntityType],
    uc: FromDishka[UsecaseCategoryDeleteType],
    uuid: CategoryId,
) -> CategoryDeleteSchema:
    result = await uc.execute(user=user, category_uuid=uuid)
    return CategoryDeleteSchema.from_obj(obj=result)
