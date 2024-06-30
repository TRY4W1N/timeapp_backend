from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    APP_ENV: str
    APP_HOST: str
    APP_PORT: int
    APP_NAME: str = "TimeApp"
    DEBUG: bool = Field(default=False)
    FIREBASE_SECRET_PATH: str

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

    @property
    def MONGODB_URL(self) -> str:
        auth_block = ""
        if all([self.MONGODB_USERNAME, self.MONGODB_PASSWORD]):
            auth_block = f"{self.MONGODB_USERNAME}:{self.MONGODB_PASSWORD}@"
        return f"mongodb://{auth_block}{self.MONGODB_HOST}:{self.MONGODB_PORT}?authSource={self.MONGODB_DATABASE}&retryWrites=true&w=majority"


class ConfigLocal(ConfigBase):
    model_config = SettingsConfigDict(env_file="local.env", env_file_encoding="utf-8", extra="ignore")


class ConfigDocker(ConfigBase):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
