from src.domain.common.exception.base import EntityNotFound
from src.domain.common.interface.usecase.base import Usecase
from src.domain.ctx.auth.interface.service import AuthService
from src.domain.ctx.user.dto import UserCreateDTO
from src.domain.ctx.user.entity import UserEntity
from src.domain.ctx.user.interface.gateway import UserGateway
from src.domain.ctx.user.interface.types import UserId


class UsecaseUserGetByToken(Usecase):

    def __init__(self, auth_service: AuthService, user_gateway: UserGateway) -> None:
        self.auth_service = auth_service
        self.user_gateway = user_gateway

    async def execute(self, token: str) -> UserEntity:
        user_identity = await self.auth_service.get_by_token(token=token)
        user_uuid = UserId(user_identity.id)
        try:
            user_entity = await self.user_gateway.get(uuid=user_uuid)
            print(f"Exist user: {user_entity}")
        except EntityNotFound:
            user = UserCreateDTO(
                uuid=user_uuid,
                name=user_identity.name,
                email=user_identity.email,
            )
            user_entity = await self.user_gateway.create(user=user)
            print(f"Create user: {user_entity}")
        return user_entity
