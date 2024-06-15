from typing import Annotated

from dishka import FromComponent

from src.domain.ctx.auth.gateway import AuthGateway
from src.infrastructure.database.mongodb.database import DatabaseMongo
from src.infrastructure.di.config import Config


AuthType = Annotated[AuthGateway, FromComponent("AUTH")]
ConfigType = Annotated[Config, FromComponent("CONFIG")]
DatabaseMongoType = Annotated[DatabaseMongo, FromComponent("DATABASE")]
