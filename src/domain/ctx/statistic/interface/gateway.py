from abc import ABC, abstractmethod

from src.domain.ctx.statistic.dto import (
    ListCategoryTimeStatisticDTO,
    StatisticFilterDTO,
)
from src.domain.ctx.user.entity import UserEntity


class StatisticGateway(ABC):

    @abstractmethod
    async def get_categories_statistic(
        self, user: UserEntity, fltr: StatisticFilterDTO
    ) -> ListCategoryTimeStatisticDTO:
        """Get statistic for categories

        Args:
            user (UserEntity): User entity
            fltr (StatisticFilterDTO): Filter for statistic categories

        Returns:
            ListCategoryTimeStatisticDTO: Category statistic list of user
        """
