import os

from dishka import Provider, Scope, provide

from src.infrastructure.config import ConfigBase, ConfigDocker, ConfigLocal, EnvType


class ConfigProvider(Provider):
    component = "CONFIG"

    @provide(scope=Scope.APP)
    def get_config(self) -> ConfigBase:
        env = os.environ.get("ENV", "").upper()
        config = None
        if env == EnvType.DOCKER.value:
            config = ConfigDocker()  # type: ignore
        if env == EnvType.LOCAL.value:
            config = ConfigLocal()  # type: ignore
        if config is None:
            raise ValueError("Invalid environment")
        return config
