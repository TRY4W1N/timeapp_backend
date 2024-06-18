from typing import Annotated, NewType

from dishka import FromComponent

from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.user.entity import UserEntity
from src.domain.usecases.category.clear import UsecaseCategoryClear
from src.domain.usecases.category.create import UsecaseCategoryCreate
from src.domain.usecases.category.delete import UsecaseCategoryDelete
from src.domain.usecases.category.get_list import UsecaseCategoryGetList
from src.domain.usecases.category.track_start import UsecaseCategoryTrackStart
from src.domain.usecases.category.track_stop import UsecaseCategoryTrackStop
from src.domain.usecases.category.update import UsecaseCategoryUpdate
from src.infrastructure.config import Config
from src.infrastructure.database.mongodb.database import DatabaseMongo

UserToken = NewType("UserToken", str)

ConfigType = Annotated[Config, FromComponent("CONFIG")]
DatabaseMongoType = Annotated[DatabaseMongo, FromComponent("DATABASE")]
UserTokenType = Annotated[UserToken, FromComponent("REQUEST")]
UserEntityType = Annotated[UserEntity, FromComponent("REQUEST")]

# Gateways
GatewayCategoryType = Annotated[CategoryGateway, FromComponent("GATEWAY")]
GatewayIntervalType = Annotated[IntervalGateway, FromComponent("GATEWAY")]

# Usecases
UsecaseCategoryCreateType = Annotated[
    UsecaseCategoryCreate,
    FromComponent("USECASE"),
]
UsecaseCategoryClearType = Annotated[
    UsecaseCategoryClear,
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
UsecaseCategoryTrackStartType = Annotated[
    UsecaseCategoryTrackStart,
    FromComponent("USECASE"),
]
UsecaseCategoryTrackStopType = Annotated[
    UsecaseCategoryTrackStop,
    FromComponent("USECASE"),
]
