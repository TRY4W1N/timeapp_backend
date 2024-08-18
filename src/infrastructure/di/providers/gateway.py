from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide

from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.statistic.interface.gateway import StatisticGateway
from src.domain.ctx.user.interface.gateway import UserGateway
from src.infrastructure.database.mongodb.gateways.category import CategoryGatewayMongo
from src.infrastructure.database.mongodb.gateways.interval import IntervalGatewayMongo
from src.infrastructure.database.mongodb.gateways.statistic import StatisticGatewayMongo
from src.infrastructure.database.mongodb.gateways.user import UserGatewayMongo
from src.infrastructure.di.alias import ConfigType, DatabaseMongoType


class GatewayProvider(Provider):
    component = "GATEWAY"

    @provide(scope=Scope.REQUEST)
    async def get_statistic(self, database: DatabaseMongoType, config: ConfigType) -> AsyncIterable[StatisticGateway]:
        category_collection = database.get_collection(config.MONGODB_COLLECTION_CATEGORY)
        interval_collection = database.get_collection(config.MONGODB_COLLECTION_INTERVAL)
        time_all_collection = database.get_collection(config.MONGODB_COLLECTION_TIMEALL)
        time_day_collection = database.get_collection(config.MONGODB_COLLECTION_TIMEDAY)
        gateway = StatisticGatewayMongo(
            category_collection=category_collection,
            interval_collection=interval_collection,
            time_all_collection=time_all_collection,
            time_day_collection=time_day_collection,
        )
        yield gateway

    @provide(scope=Scope.REQUEST)
    async def get_category(self, database: DatabaseMongoType, config: ConfigType) -> AsyncIterable[CategoryGateway]:
        category_collection = database.get_collection(config.MONGODB_COLLECTION_CATEGORY)
        interval_collection = database.get_collection(config.MONGODB_COLLECTION_INTERVAL)
        time_all_collection = database.get_collection(config.MONGODB_COLLECTION_TIMEALL)
        time_day_collection = database.get_collection(config.MONGODB_COLLECTION_TIMEDAY)
        gateway = CategoryGatewayMongo(
            category_collection=category_collection,
            interval_collection=interval_collection,
            time_all_collection=time_all_collection,
            time_day_collection=time_day_collection,
        )
        yield gateway

    @provide(scope=Scope.REQUEST)
    async def get_interval(self, database: DatabaseMongoType, config: ConfigType) -> AsyncIterable[IntervalGateway]:
        interval_collection = database.get_collection(config.MONGODB_COLLECTION_INTERVAL)
        category_collection = database.get_collection(config.MONGODB_COLLECTION_CATEGORY)
        gateway = IntervalGatewayMongo(category_collection=category_collection, interval_collection=interval_collection)
        yield gateway

    @provide(scope=Scope.REQUEST)
    async def get_user(self, database: DatabaseMongoType, config: ConfigType) -> AsyncIterable[UserGateway]:
        user_collection = database.get_collection(config.MONGODB_COLLECTION_USER)
        category_collection = database.get_collection(config.MONGODB_COLLECTION_CATEGORY)
        gateway = UserGatewayMongo(user_collection=user_collection, category_collection=category_collection)
        yield gateway
