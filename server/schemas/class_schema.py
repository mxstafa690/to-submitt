from datetime import datetime
from pydantic import BaseModel, Field


class ClassCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    instructor: str = Field(min_length=2, max_length=120)
    start_time: datetime
    duration_minutes: int = Field(default=60, ge=15, le=300)
    capacity: int = Field(default=20, ge=1, le=300)


class ClassResponse(BaseModel):
    id: int
    title: str
    instructor: str
    start_time: datetime
    duration_minutes: int
    capacity: int
    created_at: datetime
