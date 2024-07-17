from abc import ABC, abstractmethod

from src.domain.ctx.time_all.dto import ListCategoryTimeStatistic
from src.domain.ctx.user.entity import UserEntity


class TimeAllGateway(ABC):

    @abstractmethod
    async def get_categories_statistic(self, user: UserEntity) -> ListCategoryTimeStatistic:
        """Get statistic for categories

        Args:
            user_uuid (str): User uuid

        Returns:
            ListCategoryTimeStatistic: Category statistic list of user
        """
