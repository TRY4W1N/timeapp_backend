from dishka import AsyncContainer, make_async_container

from src.infrastructure.di.providers.config import ConfigProvider
from src.infrastructure.di.providers.database import DatabaseProvider
from src.infrastructure.di.providers.gateway import GatewayProvider


def build_container() -> AsyncContainer:
    return make_async_container(ConfigProvider(), DatabaseProvider(), GatewayProvider())
