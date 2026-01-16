from pydantic import BaseModel, Field, field_validator
from config.constants import PaymentStatus


class PaymentCreate(BaseModel):
    subscription_id: int = Field(gt=0)
    amount: float = Field(gt=0)
    reference: str | None = Field(default=None, max_length=120)


class PaymentStatusUpdate(BaseModel):
    status: str = Field(min_length=3, max_length=20)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str):
        v = v.strip().lower()
        if v not in PaymentStatus.values():
            raise ValueError(f"status must be one of: {', '.join(PaymentStatus.values())}")
        return v
