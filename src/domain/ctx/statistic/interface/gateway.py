from abc import ABC, abstractmethod

from src.domain.ctx.statistic.dto import (
    ListCategoryTimeStatisticDTO,
    StatisticFilterTimeDayDTO,
)
from src.domain.ctx.user.entity import UserEntity


class StatisticGateway(ABC):

    @abstractmethod
    async def get_categories_statistic(
        self, user: UserEntity, fltr: StatisticFilterTimeDayDTO
    ) -> ListCategoryTimeStatisticDTO:
        """Get statistic for categories

        Args:
            user (UserEntity): User entity
            fltr (StatisticFilterTimeDayDTO): Filter for statistic time day

        Returns:
            ListCategoryTimeStatisticDTO: Category statistic list of user
        """
