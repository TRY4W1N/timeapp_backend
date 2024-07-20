from pydantic import BaseModel

from src.domain.ctx.statistic.dto import ListCategoryTimeStatisticDTO


class CategoryTimeStatisticSchema(BaseModel):
    category_uuid: str
    total_time: int
    time_percent: float


class ListCategoryTimeStatisticSchema(BaseModel):
    user_uuid: str
    category_list: list[CategoryTimeStatisticSchema]

    @classmethod
    def from_obj(cls, obj_list: ListCategoryTimeStatisticDTO) -> "ListCategoryTimeStatisticSchema":
        category_list = [
            CategoryTimeStatisticSchema(
                category_uuid=category.category_uuid, time_percent=category.time_percent, total_time=category.total_time
            )
            for category in obj_list.category_list
        ]
        return ListCategoryTimeStatisticSchema(user_uuid=obj_list.user_uuid, category_list=category_list)
