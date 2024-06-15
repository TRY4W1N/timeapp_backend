from typing import Annotated

from dishka import FromComponent

from src.domain.ctx.auth.gateway import AuthGateway

AuthType = Annotated[AuthGateway, FromComponent("AUTH")]