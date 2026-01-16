from typing import Optional
from pydantic import BaseModel, Field
from config.constants import (
    MIN_NAME_LENGTH,
    MAX_NAME_LENGTH,
    EMAIL_REGEX,
    PHONE_REGEX,
    MAX_STATUS_LENGTH
)


class UserResponse(BaseModel):
    """Base response schema for User entity."""
    id: int
    role: str
    full_name: str
    email: str
    phone: str
    status: str
    created_at: str

    class Config:
        from_attributes = True
