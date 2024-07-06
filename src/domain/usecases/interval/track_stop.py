from src.domain.common.interface.usecase.base import Usecase
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import IntervalStopDTO
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.user.entity import UserEntity


class UsecaseIntervalTrackStop(Usecase):

    def __init__(self, interval_gateway: IntervalGateway) -> None:
        self.interval_gateway = interval_gateway

    async def execute(self, user: UserEntity, category_uuid: CategoryId, stopped_at: int) -> IntervalStopDTO:
        interval_stop = await self.interval_gateway.stop(user=user, category_uuid=category_uuid, stopped_at=stopped_at)
        return interval_stop
