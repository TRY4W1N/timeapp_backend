from src.domain.common.interface.usecase.base import Usecase
from src.domain.ctx.category.dto import CategoryAddDTO
from src.domain.ctx.category.entity import CategoryEntity
from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.user.entity import UserEntity


class UsecaseCategoryAdd(Usecase):

    def __init__(self, category_gateway: CategoryGateway) -> None:
        self.category_gateway = category_gateway

    async def execute(self, user: UserEntity, obj: CategoryAddDTO) -> CategoryEntity:
        category_entity = await self.category_gateway.add(user_uuid=user.uuid, obj=obj)
        return category_entity
