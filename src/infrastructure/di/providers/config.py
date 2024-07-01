import os

from dishka import Provider, Scope, provide

from src.infrastructure.config import ConfigBase, ConfigDocker, ConfigLocal


class ConfigProvider(Provider):
    component = "CONFIG"

    @provide(scope=Scope.APP)
    def get_config(self) -> ConfigBase:
        if os.environ.get("APP_ENV", "").upper() == "DOCKER":
            return ConfigDocker()  # type: ignore
        return ConfigLocal()  # type: ignore
