from dataclasses import dataclass

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.interface.types import UserId


@dataclass
class CategoryEntity:
    uuid: CategoryId
    user_uuid: UserId
    name: str
    disabled: bool
    icon: str
    icon_color: str
    position: int
    on_track: bool
