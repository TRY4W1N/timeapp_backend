from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide

from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.infrastructure.database.mongodb.gateways.category import CategoryGatewayMongo
from src.infrastructure.di.alias import ConfigType, DatabaseMongoType


class GatewayProvider(Provider):
    component = "GATEWAY"

    @provide(scope=Scope.REQUEST)
    async def get_category(self, database: DatabaseMongoType, config: ConfigType) -> AsyncIterable[CategoryGateway]:
        collection = database.get_collection(config.MONGODB_COLLECTION_CATEGORY)
        gateway = CategoryGatewayMongo(collection=collection)
        yield gateway
