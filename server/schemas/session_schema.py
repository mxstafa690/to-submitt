from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    member_id: int = Field(gt=0)
