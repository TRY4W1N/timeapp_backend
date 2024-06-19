from src.domain.common.interface.usecase.base import Usecase
from src.domain.ctx.category.dto import CategoryDeleteDTO
from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.entity import UserEntity


class UsecaseCategoryDelete(Usecase):

    def __init__(self, category_gateway: CategoryGateway) -> None:
        self.category_gateway = category_gateway

    async def execute(self, user: UserEntity, category_uuid: CategoryId) -> CategoryDeleteDTO:
        result = await self.category_gateway.delete(user_uuid=user.uuid, category_uuid=category_uuid)
        return result
