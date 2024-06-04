from dishka import make_async_container, AsyncContainer
from .providers.database import DatabaseProvider

def build_container() -> AsyncContainer:
    return make_async_container(
        DatabaseProvider(),
    )