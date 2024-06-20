from dishka import AsyncContainer, make_async_container

from src.infrastructure.di.providers.app_service import AppServiceProvider
from src.infrastructure.di.providers.config import ConfigProvider
from src.infrastructure.di.providers.database import DatabaseProvider
from src.infrastructure.di.providers.gateway import GatewayProvider
from src.infrastructure.di.providers.request_ctx import RequestProvider
from src.infrastructure.di.providers.usecase import UsecaseProvider


def build_container() -> AsyncContainer:
    return make_async_container(
        ConfigProvider(),
        DatabaseProvider(),
        GatewayProvider(),
        AppServiceProvider(),
        UsecaseProvider(),
        RequestProvider(),
    )
