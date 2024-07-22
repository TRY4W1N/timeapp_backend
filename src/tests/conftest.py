import asyncio
from collections.abc import AsyncGenerator

import pytest
from dishka import AsyncContainer
from pytest_mock import MockerFixture

from src.domain.ctx.auth.dto import UserIdentityDTO
from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.statistic.interface.gateway import StatisticGateway
from src.domain.ctx.user.entity import UserEntity
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.config import ConfigBase
from src.infrastructure.database.mongodb.database import DatabaseMongo
from src.infrastructure.di.container import build_container
from src.tests.dataloader import Dataloader


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def dicon() -> AsyncGenerator[AsyncContainer, None]:
    container = build_container()
    try:
        async with container() as _container:
            yield _container
    finally:
        await container.close()


@pytest.fixture(scope="function")
async def dl(dicon: AsyncContainer) -> AsyncGenerator[Dataloader, None]:
    database = await dicon.get(DatabaseMongo, component="DATABASE")
    config = await dicon.get(ConfigBase, component="CONFIG")
    async with Dataloader(database=database, config=config) as _dl:
        yield _dl


@pytest.fixture(scope="function")
async def fx_user(dl: Dataloader) -> AsyncGenerator[UserEntity, None]:
    user_model = await dl.user_loader.create()
    yield UserEntity(uuid=UserId(user_model.uuid), email=user_model.email, name=user_model.name)


@pytest.fixture(scope="function")
async def gateway_category(dicon: AsyncContainer) -> AsyncGenerator[CategoryGateway, None]:
    yield await dicon.get(CategoryGateway, component="GATEWAY")


@pytest.fixture(scope="function")
async def gateway_interval(dicon: AsyncContainer) -> AsyncGenerator[IntervalGateway, None]:
    yield await dicon.get(IntervalGateway, component="GATEWAY")


@pytest.fixture(scope="function")
async def gateway_time_all(dicon: AsyncContainer) -> AsyncGenerator[StatisticGateway, None]:
    yield await dicon.get(StatisticGateway, component="GATEWAY")


@pytest.fixture(scope="function")
async def mock_auth_service_get_by_token(
    mocker: MockerFixture, fx_user: UserEntity
) -> AsyncGenerator[UserIdentityDTO, None]:
    user_identity_static = UserIdentityDTO(
        id=fx_user.uuid,
        name=fx_user.name,
        email=fx_user.email,
    )
    mocker.patch(
        "src.application.service.auth.firebase.service.AuthServiceFirebase.get_by_token",
        return_value=user_identity_static,
    )
    yield user_identity_static
