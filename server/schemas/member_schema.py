from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re
from config.constants import (
    EMAIL_REGEX,
    PHONE_REGEX,
    NATIONAL_ID_REGEX,
    MIN_NAME_LENGTH,
    MAX_NAME_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_LOWERCASE_PATTERN,
    PASSWORD_UPPERCASE_PATTERN,
    PASSWORD_DIGIT_PATTERN,
    PASSWORD_SPECIAL_PATTERN,
    MemberStatus,
    MAX_STATUS_LENGTH
)


class MemberCreate(BaseModel):
    full_name: str = Field(min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    email: str = Field(pattern=EMAIL_REGEX)
    phone: str = Field(pattern=PHONE_REGEX)
    national_id: str = Field(pattern=NATIONAL_ID_REGEX)
    password: str = Field(min_length=PASSWORD_MIN_LENGTH)

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


class MemberUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    email: Optional[str] = Field(default=None, pattern=EMAIL_REGEX)
    phone: Optional[str] = Field(default=None, pattern=PHONE_REGEX)
    status: Optional[str] = Field(default=None, max_length=MAX_STATUS_LENGTH)
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]):
        if v is not None and v not in MemberStatus.values():
            raise ValueError(f"Status must be one of: {', '.join(MemberStatus.values())}")
        return v
