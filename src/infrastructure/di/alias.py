from typing import Annotated, NewType

from dishka import FromComponent

from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.user.entity import UserEntity
from src.domain.usecases.category.add import UsecaseCategoryAdd
from src.infrastructure.config import Config
from src.infrastructure.database.mongodb.database import DatabaseMongo

UserToken = NewType("UserToken", str)

ConfigType = Annotated[Config, FromComponent("CONFIG")]
DatabaseMongoType = Annotated[DatabaseMongo, FromComponent("DATABASE")]
UserTokenType = Annotated[UserToken, FromComponent("REQUEST")]
UserEntityType = Annotated[UserEntity, FromComponent("REQUEST")]

# Gateways
GatewayCategoryType = Annotated[CategoryGateway, FromComponent("GATEWAY")]

# Usecases
UsecaseCategoryAddType = Annotated[
    UsecaseCategoryAdd,
    FromComponent("USECASE"),
]
