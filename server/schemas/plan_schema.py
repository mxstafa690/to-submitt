from pydantic import BaseModel, Field
from config.constants import MIN_NAME_LENGTH


class PlanCreate(BaseModel):
    name: str = Field(min_length=MIN_NAME_LENGTH, max_length=120)
    type: str = Field(min_length=3, max_length=30)
    price: float = Field(gt=0)
    valid_days: int = Field(gt=0)
    max_entries: int | None = Field(default=None, gt=0)
