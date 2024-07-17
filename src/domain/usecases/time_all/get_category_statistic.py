from src.domain.ctx.time_all.dto import ListCategoryTimeStatistic
from src.domain.ctx.time_all.interface.gateway import TimeAllGateway
from src.domain.ctx.user.entity import UserEntity


class GetCategoryStatisticUsecase:
    def __init__(self, time_all_gateway: TimeAllGateway) -> None:
        self.time_all_gateway = time_all_gateway

    async def execute(self, user: UserEntity) -> ListCategoryTimeStatistic:
        res = await self.time_all_gateway.get_categories_statistic(user=user)
        return res
