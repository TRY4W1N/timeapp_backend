from uuid import uuid4
from motor.motor_asyncio import AsyncIOMotorCollection

MongoCollectionType = AsyncIOMotorCollection

class GatewayBaseImp:

    def gen_uuid(self) -> str:
        return str(uuid4())
