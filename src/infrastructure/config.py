import json

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    APP_NAME: str = "TimeApp"
    APP_ENV: str = "DEV"
    DEBUG: bool = Field(default=False)
    FIREBASE_SECRET_PATH: str = Field(default="")

    MONGODB_URL: str = "mongodb://127.0.0.1?retryWrites=true&w=majority"
    MONGODB_DATABASE: str = "timeappdb"
    MONGODB_COLLECTION_USER: str = Field(default="User")
    MONGODB_COLLECTION_CATEGORY: str = Field(default="Category")
    MONGODB_COLLECTION_INTERVAL: str = Field(default="Interval")
    MONGODB_COLLECTION_TIMEDAY: str = Field(default="TimeDay")
    MONGODB_COLLECTION_TIMEALL: str = Field(default="TimeAll")

    DEV_USERS_JSON_PATH: str = Field(default="")

    @field_validator("APP_ENV")
    @classmethod
    def app_env_upper(cls, v: str) -> str:
        return v.upper()

    @property
    def DEV_USERS(self) -> dict:
        if self.APP_ENV != "DEV" or not self.DEV_USERS_JSON_PATH:
            raise NotImplementedError("Used only in `DEV`")
        with open(self.DEV_USERS_JSON_PATH) as f:
            data = json.load(f)
        return data

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")