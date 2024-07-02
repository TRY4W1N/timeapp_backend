from pydantic import BaseModel


class HealCheckDatabaseSchema(BaseModel):
    version: str
