import os

from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str
    CONFIGURE_JSON_PATH: str = ""

    FIREBASE_SECRET_PATH: str
    FIREBASE_APP_NAME: str

    class Config:
        env_file = ".env"

    @field_validator("CONFIGURE_JSON_PATH")
    def conf_json_path_exist(cls, v: str) -> str:
        if not os.path.exists(v):
            raise Exception(f"Please create file {v} for setup app!")
        return v


class SettingsDev(Settings):
    CONFIGURE_JSON_PATH: str = "develop.json"

    class Config:
        env_file = "dev.env"


class SettingsTest(Settings):
    CONFIGURE_JSON_PATH: str = "test.json"

    class Config:
        env_file = "test.env"


class SettingsProd(Settings):
    CONFIGURE_JSON_PATH: str = "prod.json"

    class Config:
        env_file = "prod.env"


config = dict(dev=SettingsDev, test=SettingsTest, prod=SettingsProd)
settings: Settings = config[os.environ.get("APP_ENV", "dev").lower()]()  # type: ignore
 
