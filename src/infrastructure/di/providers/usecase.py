from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide

from src.domain.usecases.category.add import UsecaseCategoryAdd
from src.infrastructure.di.alias import GatewayCategoryType  # , UserTokenType


class UsecaseProvider(Provider):
    component = "USECASE"

    @provide(scope=Scope.REQUEST)
    async def get_category_add(
        self,
        gateway: GatewayCategoryType,  # token: UserTokenType
    ) -> AsyncIterable[UsecaseCategoryAdd]:
        yield UsecaseCategoryAdd(category_gateway=gateway)
