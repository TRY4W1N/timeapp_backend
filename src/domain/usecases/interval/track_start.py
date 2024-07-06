from src.domain.common.interface.usecase.base import Usecase
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import IntervalStartDTO
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.user.entity import UserEntity


class UsecaseIntervalTrackStart(Usecase):

    def __init__(self, interval_gateway: IntervalGateway) -> None:
        self.interval_gateway = interval_gateway

    async def execute(self, user: UserEntity, category_uuid: CategoryId, started_at: int) -> IntervalStartDTO:
        interval_start = await self.interval_gateway.start(
            user=user, category_uuid=category_uuid, started_at=started_at
        )
        return interval_start
