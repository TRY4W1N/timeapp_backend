from enum import Enum
import json

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvType(str, Enum):
    LOCAL = "LOCAL"
    DOCKER = "DOCKER"

class AppEnvType(str, Enum):
    DEV = "DEV"
    PROD = "PROD"

class ConfigBase(BaseSettings):
    ENV: str
    APP_ENV: str
    APP_HOST: str
    APP_PORT: int
    APP_NAME: str = "TimeApp"
    DEBUG: bool = Field(default=False)
    FIREBASE_SECRET_PATH: str
    DEV_USERS_JSON_PATH: str

    MONGODB_HOST: str
    MONGODB_PORT: str
    MONGODB_USERNAME: str | None = None
    MONGODB_PASSWORD: str | None = None
    MONGODB_DATABASE: str
    MONGODB_COLLECTION_USER: str
    MONGODB_COLLECTION_CATEGORY: str
    MONGODB_COLLECTION_INTERVAL: str
    MONGODB_COLLECTION_TIMEDAY: str
    MONGODB_COLLECTION_TIMEALL: str

    @field_validator("APP_ENV")
    @classmethod
    def app_env_upper(cls, v: str) -> str:
        if v not in [e.value for e in AppEnvType]:
            raise ValueError(f"Invalid APP_ENV value: {v}")
        return v.upper()

    @field_validator("ENV")
    @classmethod
    def env_upper(cls, v: str) -> str:
        if v not in [e.value for e in EnvType]:
            raise ValueError(f"Invalid ENV value: {v}")
        return v.upper()

    @property
    def MONGODB_URL(self) -> str:
        auth_block = ""
        if all([self.MONGODB_USERNAME, self.MONGODB_PASSWORD]):
            auth_block = f"{self.MONGODB_USERNAME}:{self.MONGODB_PASSWORD}@"
        return f"mongodb://{auth_block}{self.MONGODB_HOST}:{self.MONGODB_PORT}?authSource={self.MONGODB_DATABASE}&retryWrites=true&w=majority"

    @property
    def DEV_USERS(self) -> dict:
        if self.APP_ENV != "DEV" or not self.DEV_USERS_JSON_PATH:
            raise NotImplementedError("Used only in `APP_ENV=DEV`")
        with open(self.DEV_USERS_JSON_PATH) as f:
            data = json.load(f)
        return data


class ConfigLocal(ConfigBase):
    model_config = SettingsConfigDict(env_file="local.env", env_file_encoding="utf-8", extra="ignore")


class ConfigDocker(ConfigBase):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
