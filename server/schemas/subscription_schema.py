from datetime import date
from pydantic import BaseModel, Field


class SubscriptionCreate(BaseModel):
    plan_id: int = Field(gt=0)
    start_date: date | None = None


class FreezeRequest(BaseModel):
    days: int = Field(gt=0, le=365)
