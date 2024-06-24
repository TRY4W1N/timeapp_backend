from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide

from src.domain.usecases.category.create import UsecaseCategoryCreate
from src.domain.usecases.category.delete import UsecaseCategoryDelete
from src.domain.usecases.category.get_list import UsecaseCategoryGetList
from src.domain.usecases.category.update import UsecaseCategoryUpdate
from src.domain.usecases.interval.clear import UsecaseIntervalClear
from src.domain.usecases.interval.track_start import UsecaseIntervalTrackStart
from src.domain.usecases.interval.track_stop import UsecaseIntervalTrackStop
from src.domain.usecases.user.user_get_by_token import UsecaseUserGetByToken
from src.infrastructure.di.alias import (
    GatewayCategoryType,
    GatewayIntervalType,
    GatewayUserType,
    ServiceAuthType,
)


class UsecaseProvider(Provider):
    component = "USECASE"

    @provide(scope=Scope.REQUEST)
    async def get_user_get_by_token(
        self,
        auth_service: ServiceAuthType,
        gateway: GatewayUserType,
    ) -> AsyncIterable[UsecaseUserGetByToken]:
        yield UsecaseUserGetByToken(auth_service=auth_service, user_gateway=gateway)

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
    async def get_interval_clear(
        self,
        gateway: GatewayIntervalType,
    ) -> AsyncIterable[UsecaseIntervalClear]:
        yield UsecaseIntervalClear(interval_gateway=gateway)

    @provide(scope=Scope.REQUEST)
    async def get_category_get_list(
        self,
        gateway: GatewayCategoryType,
    ) -> AsyncIterable[UsecaseCategoryGetList]:
        yield UsecaseCategoryGetList(category_gateway=gateway)

    @provide(scope=Scope.REQUEST)
    async def get_interval_track_start(
        self,
        gateway: GatewayIntervalType,
    ) -> AsyncIterable[UsecaseIntervalTrackStart]:
        yield UsecaseIntervalTrackStart(interval_gateway=gateway)

    @provide(scope=Scope.REQUEST)
    async def get_interval_track_stop(
        self,
        gateway: GatewayIntervalType,
    ) -> AsyncIterable[UsecaseIntervalTrackStop]:
        yield UsecaseIntervalTrackStop(interval_gateway=gateway)
