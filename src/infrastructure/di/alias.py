from typing import Annotated
from dishka import FromComponent

from src.infrastructure.database.mongodb.database import DatabaseMongo
from src.infrastructure.di.config import Config


ConfigType = Annotated[Config, FromComponent("CONFIG")]
DatabaseMongoType = Annotated[DatabaseMongo, FromComponent("DATABASE")]