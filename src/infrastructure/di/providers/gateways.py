from collections.abc import AsyncIterable
from dishka import Provider, Scope, provide

from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.infrastructure.database.mongodb.gateways.category import CategoryGatewayImp
from src.infrastructure.di.alias import DatabaseMongoType


class GatewayProvider(Provider):
    component = "GATEWAY"

    @provide(scope=Scope.REQUEST)
    async def get_category(self, database: DatabaseMongoType) -> AsyncIterable[CategoryGateway]:
        collection = database.get_collection("Category")
        gateway = CategoryGatewayImp(collection=collection)
        yield gateway
    