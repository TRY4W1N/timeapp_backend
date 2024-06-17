from collections.abc import AsyncGenerator

import pytest
from dishka import AsyncContainer

from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.infrastructure.config import Config
from src.infrastructure.database.mongodb.database import DatabaseMongo
from src.infrastructure.di.container import build_container
from src.tests.dataloader import Dataloader


@pytest.fixture(scope="session")
async def dicon() -> AsyncGenerator[AsyncContainer, None]:
    container = build_container()
    async with container() as _container:
        yield _container
    await container.close()


@pytest.fixture(scope="function")
async def dl(dicon: AsyncContainer) -> AsyncGenerator[Dataloader, None]:
    database = await dicon.get(DatabaseMongo, component="DATABASE")
    config = await dicon.get(Config, component="CONFIG")
    async with Dataloader(database=database, config=config) as _dl:
        yield _dl


@pytest.fixture(scope="function")
async def gateway_category(dicon: AsyncContainer) -> AsyncGenerator[CategoryGateway, None]:
    yield await dicon.get(CategoryGateway, component="GATEWAY")
