from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide

from src.domain.usecases.category.clear import UsecaseCategoryClear
from src.domain.usecases.category.create import UsecaseCategoryCreate
from src.domain.usecases.category.delete import UsecaseCategoryDelete
from src.domain.usecases.category.get_list import UsecaseCategoryGetList
from src.domain.usecases.category.track_start import UsecaseCategoryTrackStart
from src.domain.usecases.category.track_stop import UsecaseCategoryTrackStop
from src.domain.usecases.category.update import UsecaseCategoryUpdate
from src.infrastructure.di.alias import GatewayCategoryType, GatewayIntervalType


class UsecaseProvider(Provider):
    component = "USECASE"

    @provide(scope=Scope.REQUEST)
    async def get_category_create(
        self,
        gateway: GatewayCategoryType,
    ) -> AsyncIterable[UsecaseCategoryCreate]:
        yield UsecaseCategoryCreate(category_gateway=gateway)

    @provide(scope=Scope.REQUEST)
    async def get_category_delete(
        self,
        gateway: GatewayCategoryType,
    ) -> AsyncIterable[UsecaseCategoryDelete]:
        yield UsecaseCategoryDelete(category_gateway=gateway)

    @provide(scope=Scope.REQUEST)
    async def get_category_update(
        self,
        gateway: GatewayCategoryType,
    ) -> AsyncIterable[UsecaseCategoryUpdate]:
        yield UsecaseCategoryUpdate(category_gateway=gateway)

    @provide(scope=Scope.REQUEST)
    async def get_category_clear(
        self,
        gateway: GatewayIntervalType,
    ) -> AsyncIterable[UsecaseCategoryClear]:
        yield UsecaseCategoryClear(interval_gateway=gateway)

    @provide(scope=Scope.REQUEST)
    async def get_category_get_list(
        self,
        gateway: GatewayCategoryType,
    ) -> AsyncIterable[UsecaseCategoryGetList]:
        yield UsecaseCategoryGetList(category_gateway=gateway)

    @provide(scope=Scope.REQUEST)
    async def get_category_track_start(
        self,
        gateway: GatewayIntervalType,
    ) -> AsyncIterable[UsecaseCategoryTrackStart]:
        yield UsecaseCategoryTrackStart(interval_gateway=gateway)

    @provide(scope=Scope.REQUEST)
    async def get_category_track_stop(
        self,
        gateway: GatewayIntervalType,
    ) -> AsyncIterable[UsecaseCategoryTrackStop]:
        yield UsecaseCategoryTrackStop(interval_gateway=gateway)
