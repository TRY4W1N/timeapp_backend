from src.domain.ctx.statistic.dto import ListCategoryTimeStatisticDTO
from src.domain.ctx.statistic.interface.gateway import StatisticGateway
from src.domain.ctx.user.entity import UserEntity


class GetCategoryStatisticUsecase:
    def __init__(self, statistic_gateway: StatisticGateway) -> None:
        self.statistic_gateway = statistic_gateway

    async def execute(self, user: UserEntity) -> ListCategoryTimeStatisticDTO:
        res = await self.statistic_gateway.get_categories_statistic(user=user)
        return res
