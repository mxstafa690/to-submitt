from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re
from config.constants import (
    PASSWORD_MIN_LENGTH,
    PASSWORD_LOWERCASE_PATTERN,
    PASSWORD_UPPERCASE_PATTERN,
    PASSWORD_DIGIT_PATTERN,
    PASSWORD_SPECIAL_PATTERN,
    MIN_NAME_LENGTH,
    MAX_NAME_LENGTH,
    EMAIL_REGEX,
    PHONE_REGEX
)


class TrainerCreate(BaseModel):
    """Schema for creating a new trainer."""
    full_name: str = Field(min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    email: str = Field(pattern=EMAIL_REGEX)
    phone: str = Field(pattern=PHONE_REGEX)
    password: str = Field(min_length=PASSWORD_MIN_LENGTH)
    specialization: Optional[str] = Field(default=None, max_length=100)
    certification: Optional[str] = Field(default=None, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if not re.search(PASSWORD_LOWERCASE_PATTERN, v):
            raise ValueError("Password must include a lowercase letter")
        if not re.search(PASSWORD_UPPERCASE_PATTERN, v):
            raise ValueError("Password must include an uppercase letter")
        if not re.search(PASSWORD_DIGIT_PATTERN, v):
            raise ValueError("Password must include a digit")
        if not re.search(PASSWORD_SPECIAL_PATTERN, v):
            raise ValueError("Password must include a special character")
        return v


class TrainerUpdate(BaseModel):
    """Schema for updating a trainer."""
    full_name: Optional[str] = Field(default=None, min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    email: Optional[str] = Field(default=None, pattern=EMAIL_REGEX)
    phone: Optional[str] = Field(default=None, pattern=PHONE_REGEX)
    specialization: Optional[str] = Field(default=None, max_length=100)
    certification: Optional[str] = Field(default=None, max_length=100)
    status: Optional[str] = Field(default=None, max_length=20)


class TrainerResponse(BaseModel):
    """Schema for trainer response."""
    id: int
    role: str
    full_name: str
    email: str
    phone: str
    specialization: Optional[str]
    certification: Optional[str]
    status: str
    created_at: str

    class Config:
        from_attributes = True
