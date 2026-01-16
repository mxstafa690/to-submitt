"""Validation utility functions for FitTrack."""
import re
from config.constants import (
    EMAIL_REGEX,
    PHONE_REGEX,
    NATIONAL_ID_REGEX,
    PASSWORD_LOWERCASE_PATTERN,
    PASSWORD_UPPERCASE_PATTERN,
    PASSWORD_DIGIT_PATTERN,
    PASSWORD_SPECIAL_PATTERN,
    PASSWORD_MIN_LENGTH
)


def validate_email(email: str) -> bool:
    """Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    return bool(re.match(EMAIL_REGEX, email))


def validate_phone(phone: str) -> bool:
    """Validate Israeli phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not phone:
        return False
    return bool(re.match(PHONE_REGEX, phone))


def validate_national_id(national_id: str) -> bool:
    """Validate Israeli national ID format (9 digits).
    
    Args:
        national_id: National ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not national_id:
        return False
    return bool(re.match(NATIONAL_ID_REGEX, national_id))


def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """Validate password strength requirements.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, list of error messages)
    """
    errors = []
    
    if len(password) < PASSWORD_MIN_LENGTH:
        errors.append(f"Password must be at least {PASSWORD_MIN_LENGTH} characters long")
    
    if not re.search(PASSWORD_LOWERCASE_PATTERN, password):
        errors.append("Password must include a lowercase letter")
    
    if not re.search(PASSWORD_UPPERCASE_PATTERN, password):
        errors.append("Password must include an uppercase letter")
    
    if not re.search(PASSWORD_DIGIT_PATTERN, password):
        errors.append("Password must include a digit")
    
    if not re.search(PASSWORD_SPECIAL_PATTERN, password):
        errors.append("Password must include a special character")
    
    return (len(errors) == 0, errors)


def sanitize_string(value: str) -> str:
    """Sanitize string by trimming whitespace.
    
    Args:
        value: String to sanitize
        
    Returns:
        Sanitized string
    """
    if not value:
        return ""
    return value.strip()


def normalize_email(email: str) -> str:
    """Normalize email to lowercase and trim whitespace.
    
    Args:
        email: Email to normalize
        
    Returns:
        Normalized email
    """
    if not email:
        return ""
    return email.strip().lower()
