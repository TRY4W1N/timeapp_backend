from dataclasses import dataclass, fields

from src.domain.common.dto.unset import UnsetDTO


@dataclass
class FltrDTO(UnsetDTO):
    @property
    def _count_fields(self) -> int:
        return len(fields(self))
