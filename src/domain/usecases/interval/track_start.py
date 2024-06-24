from src.domain.common.interface.usecase.base import Usecase
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import IntervalStartDTO
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.user.entity import UserEntity


class UsecaseIntervalTrackStart(Usecase):

    def __init__(self, interval_gateway: IntervalGateway) -> None:
        self.interval_gateway = interval_gateway

    async def execute(self, user: UserEntity, category_uuid: CategoryId) -> IntervalStartDTO:
        interval_start = await self.interval_gateway.start(user_uuid=user.uuid, category_uuid=category_uuid)
        return interval_start
