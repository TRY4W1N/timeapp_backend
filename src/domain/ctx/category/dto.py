from dataclasses import dataclass


@dataclass
class CategoryAddDTO:
    name: str
    icon: str
    icon_color: str
    position: int
