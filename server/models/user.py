from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, Date
from services.db import Base
from config.constants import DEFAULT_MEMBER_STATUS


class User(Base):
    """
    Base User model using SQLAlchemy joined-table inheritance.
    All user types (Member, Trainer, Admin, Reception) inherit from this base class.
    Common fields are stored in the 'users' table.
    
    User types:
    - Member: Gym members with subscriptions
    - Trainer: Can manage classes, sessions, and workout plans
    - Admin: Can manage members, finances, and plans (inherits from Trainer)
    - Reception: Can handle check-ins and member registrations
    
    Supported roles: 'member', 'trainer', 'admin', 'reception'
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role = Column(String(50), nullable=False)  # Discriminator column (includes 'reception')
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default=DEFAULT_MEMBER_STATUS.value)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Configure polymorphic inheritance
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": role,
    }

    # Common methods for all user types
    def is_active(self) -> bool:
        """Check if the user account is active."""
        return self.status == "active"

    def get_role(self) -> str:
        """Get the user's role/type."""
        return self.role

    def can_login(self) -> bool:
        """Check if user can log in (basic permission)."""
        return self.is_active()

    def get_full_name(self) -> str:
        """Get formatted full name."""
        return f"{self.first_name} {self.last_name}"

    def get_display_name(self) -> str:
        """Get formatted display name. Can be overridden by subclasses."""
        return f"{self.get_full_name()} ({self.role.upper()})"

    def to_dict(self):
        """Convert user to dictionary. Can be extended by subclasses."""
        return {
            "id": self.id,
            "role": self.role,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.get_full_name(),
            "email": self.email,
            "phone": self.phone,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
