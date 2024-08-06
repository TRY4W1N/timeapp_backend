from datetime import datetime
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorCollection

MongoCollectionType = AsyncIOMotorCollection


class GatewayMongoBase:

    def gen_uuid(self) -> str:
        return str(uuid4())

    def get_current_timestamp(self) -> int:
        return int(datetime.now().timestamp())
