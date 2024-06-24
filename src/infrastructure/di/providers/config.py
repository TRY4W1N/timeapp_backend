from dishka import Provider, Scope, provide

from src.infrastructure.config import Config


class ConfigProvider(Provider):
    component = "CONFIG"

    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return Config()
