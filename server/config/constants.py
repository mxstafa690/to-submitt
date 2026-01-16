"""Application constants and enums for FitTrack."""
from enum import Enum

# ============================================================================
# VALIDATION PATTERNS
# ============================================================================
EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
PHONE_REGEX = r"^(?:\+972|0)(?:-?\d){8,9}$"
NATIONAL_ID_REGEX = r"^\d{9}$"

# ============================================================================
# FIELD LENGTHS
# ============================================================================
MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 120
MAX_PHONE_LENGTH = 20
MAX_STATUS_LENGTH = 20
MIN_NAME_LENGTH = 2

# ============================================================================
# PASSWORD REQUIREMENTS
# ============================================================================
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_DIGIT = True
PASSWORD_REQUIRE_SPECIAL = True

# Password validation patterns
PASSWORD_LOWERCASE_PATTERN = r"[a-z]"
PASSWORD_UPPERCASE_PATTERN = r"[A-Z]"
PASSWORD_DIGIT_PATTERN = r"\d"
PASSWORD_SPECIAL_PATTERN = r"[^A-Za-z0-9]"

# ============================================================================
# STATUS ENUMS
# ============================================================================

class MemberStatus(str, Enum):
    """Member status values."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

    @classmethod
    def values(cls):
        """Return list of all status values."""
        return [status.value for status in cls]


class SubscriptionStatus(str, Enum):
    """Subscription status values."""
    ACTIVE = "active"
    FROZEN = "frozen"
    EXPIRED = "expired"
    CANCELED = "canceled"

    @classmethod
    def values(cls):
        """Return list of all status values."""
        return [status.value for status in cls]


class PaymentStatus(str, Enum):
    """Payment status values."""
    PENDING = "pending"
    PAID = "paid"
    CANCELED = "canceled"

    @classmethod
    def values(cls):
        """Return list of all status values."""
        return [status.value for status in cls]


class PaymentMethod(str, Enum):
    """Payment method values."""
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"

    @classmethod
    def values(cls):
        """Return list of all payment method values."""
        return [method.value for method in cls]


class SessionStatus(str, Enum):
    """Session status values."""
    ACTIVE = "active"
    CANCELED = "canceled"
    COMPLETED = "completed"

    @classmethod
    def values(cls):
        """Return list of all status values."""
        return [status.value for status in cls]


class DayOfWeek(str, Enum):
    """Day of week values."""
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"

    @classmethod
    def values(cls):
        """Return list of all day values."""
        return [day.value for day in cls]


class DifficultyLevel(str, Enum):
    """Workout difficulty level values."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

    @classmethod
    def values(cls):
        """Return list of all difficulty values."""
        return [level.value for level in cls]


# ============================================================================
# DEFAULT VALUES
# ============================================================================
DEFAULT_MEMBER_STATUS = MemberStatus.ACTIVE
DEFAULT_SUBSCRIPTION_STATUS = SubscriptionStatus.ACTIVE
DEFAULT_PAYMENT_STATUS = PaymentStatus.PENDING
DEFAULT_SESSION_STATUS = SessionStatus.ACTIVE
