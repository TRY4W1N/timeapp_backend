from abc import ABC, abstractmethod

from src.domain.ctx.statistic.dto import ListCategoryTimeStatisticDTO
from src.domain.ctx.user.entity import UserEntity


class StatisticGateway(ABC):

    @abstractmethod
    async def get_categories_statistic(self, user: UserEntity) -> ListCategoryTimeStatisticDTO:
        """Get statistic for categories

        Args:
            user (UserEntity): User entity

        Returns:
            ListCategoryTimeStatisticDTO: Category statistic list of user
        """
