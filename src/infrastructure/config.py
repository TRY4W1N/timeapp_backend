from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_NAME: str = "TimeApp"
    DEBUG: bool = Field(default=False)
    FIREBASE_SECRET_PATH: str = Field(default="")

    MONGODB_URL: str = "mongodb://127.0.0.1?retryWrites=true&w=majority"
    MONGODB_DATABASE: str = "timeappdb"
    MONGODB_COLLECTION_USER: str = Field(default="User")
    MONGODB_COLLECTION_CATEGORY: str = Field(default="Category")
    MONGODB_COLLECTION_INTERVAL: str = Field(default="Interval")
    MONGODB_COLLECTION_TIMEDAY: str = Field(default="TimeDay")
    MONGODB_COLLECTION_TIMEALL: str = Field(default="TimeAll")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
