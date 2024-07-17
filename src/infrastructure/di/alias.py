from typing import Annotated, NewType

from dishka import FromComponent
from motor.motor_asyncio import AsyncIOMotorClient

from src.domain.ctx.auth.interface.service import AuthService
from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.user.entity import UserEntity
from src.domain.ctx.user.interface.gateway import UserGateway
from src.domain.usecases.category.create import UsecaseCategoryCreate
from src.domain.usecases.category.delete import UsecaseCategoryDelete
from src.domain.usecases.category.get_list import UsecaseCategoryGetList
from src.domain.usecases.category.update import UsecaseCategoryUpdate
from src.domain.usecases.interval.clear import UsecaseIntervalClear
from src.domain.usecases.interval.track_start import UsecaseIntervalTrackStart
from src.domain.usecases.interval.track_stop import UsecaseIntervalTrackStop
from src.domain.usecases.time_all.get_category_statistic import (
    GetCategoryStatisticUsecase,
)
from src.domain.usecases.user.user_get_by_token import UsecaseUserGetByToken
from src.infrastructure.config import ConfigBase
from src.infrastructure.database.mongodb.database import DatabaseMongo

UserToken = NewType("UserToken", str)


# Component types
ConfigType = Annotated[ConfigBase, FromComponent("CONFIG")]
MongoClientType = Annotated[
    AsyncIOMotorClient,
    FromComponent("DATABASE"),
]
DatabaseMongoType = Annotated[DatabaseMongo, FromComponent("DATABASE")]
UserTokenType = Annotated[UserToken, FromComponent("REQUEST")]
UserEntityType = Annotated[UserEntity, FromComponent("REQUEST")]

# Service Application
ServiceAuthType = Annotated[
    AuthService,
    FromComponent("SERVICE_APPLICATION"),
]

# Gateways
GatewayUserType = Annotated[UserGateway, FromComponent("GATEWAY")]
GatewayCategoryType = Annotated[CategoryGateway, FromComponent("GATEWAY")]
GatewayIntervalType = Annotated[IntervalGateway, FromComponent("GATEWAY")]

# Usecases
UsecaseUserGetByTokenType = Annotated[
    UsecaseUserGetByToken,
    FromComponent("USECASE"),
]
UsecaseCategoryCreateType = Annotated[
    UsecaseCategoryCreate,
    FromComponent("USECASE"),
]
UsecaseCategoryUpdateType = Annotated[
    UsecaseCategoryUpdate,
    FromComponent("USECASE"),
]
UsecaseCategoryDeleteType = Annotated[
    UsecaseCategoryDelete,
    FromComponent("USECASE"),
]
UsecaseCategoryGetListType = Annotated[
    UsecaseCategoryGetList,
    FromComponent("USECASE"),
]
UsecaseIntervalClearType = Annotated[
    UsecaseIntervalClear,
    FromComponent("USECASE"),
]
UsecaseIntervalTrackStartType = Annotated[
    UsecaseIntervalTrackStart,
    FromComponent("USECASE"),
]
UsecaseIntervalTrackStopType = Annotated[
    UsecaseIntervalTrackStop,
    FromComponent("USECASE"),
]
UseCaseTimeAllGetCategoryStatisticType = Annotated[GetCategoryStatisticUsecase, FromComponent("USECASE")]
