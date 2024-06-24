from src.domain.common.interface.usecase.base import Usecase
from src.domain.ctx.category.dto import CategoryUpdateDTO
from src.domain.ctx.category.entity import CategoryEntity
from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.entity import UserEntity


class UsecaseCategoryUpdate(Usecase):

    def __init__(self, category_gateway: CategoryGateway) -> None:
        self.category_gateway = category_gateway

    async def execute(self, user: UserEntity, category_uuid: CategoryId, obj: CategoryUpdateDTO) -> CategoryEntity:
        category_entity = await self.category_gateway.update(user_uuid=user.uuid, category_uuid=category_uuid, obj=obj)
        return category_entity
