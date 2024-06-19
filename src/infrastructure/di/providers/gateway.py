from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide

from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.infrastructure.database.mongodb.gateways.category import CategoryGatewayMongo
from src.infrastructure.database.mongodb.gateways.interval import IntervalGatewayMongo
from src.infrastructure.di.alias import ConfigType, DatabaseMongoType


class GatewayProvider(Provider):
    component = "GATEWAY"

    @provide(scope=Scope.REQUEST)
    async def get_category(self, database: DatabaseMongoType, config: ConfigType) -> AsyncIterable[CategoryGateway]:
        category_collection = database.get_collection(config.MONGODB_COLLECTION_CATEGORY)
        interval_collection = database.get_collection(config.MONGODB_COLLECTION_INTERVAL)
        gateway = CategoryGatewayMongo(category_collection=category_collection, interval_collection=interval_collection)
        yield gateway

    @provide(scope=Scope.REQUEST)
    async def get_interval(self, database: DatabaseMongoType, config: ConfigType) -> AsyncIterable[IntervalGateway]:
        collection = database.get_collection(config.MONGODB_COLLECTION_INTERVAL)
        gateway = IntervalGatewayMongo(collection=collection)
        yield gateway
