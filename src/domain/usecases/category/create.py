from src.domain.common.interface.usecase.base import Usecase
from src.domain.ctx.category.dto import CategoryCreateDTO
from src.domain.ctx.category.entity import CategoryEntity
from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.user.entity import UserEntity


class UsecaseCategoryCreate(Usecase):

    def __init__(self, category_gateway: CategoryGateway) -> None:
        self.category_gateway = category_gateway

    async def execute(self, user: UserEntity, obj: CategoryCreateDTO) -> CategoryEntity:
        category_entity = await self.category_gateway.create(user_uuid=user.uuid, obj=obj)
        return category_entity
