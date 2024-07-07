from src.domain.common.interface.usecase.base import Usecase
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import IntervalClearDTO
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.user.entity import UserEntity


class UsecaseIntervalClear(Usecase):

    def __init__(self, interval_gateway: IntervalGateway) -> None:
        self.interval_gateway = interval_gateway

    async def execute(self, user: UserEntity, category_uuid: CategoryId) -> IntervalClearDTO:
        interval_clear = await self.interval_gateway.clear(user=user, category_uuid=category_uuid)
        return interval_clear
