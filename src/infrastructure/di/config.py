from typing import Annotated
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PlainSerializer

ListStr = Annotated[
    str, PlainSerializer(lambda x: x.split(","), return_type=list)
]

class Config(BaseSettings):

    MONGODB_URL: str = "mongodb://127.0.0.1?retryWrites=true&w=majority"
    MONGODB_DATABASE: str = "timeappdb"
    MONGODB_COLLECTION_LIST: ListStr = Field(default_factory=list)
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

config = Config()