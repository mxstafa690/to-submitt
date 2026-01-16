from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.user import User


class Member(User):
    """
    Member model using joined-table inheritance from User.
    Member-specific data is stored in 'members' table.
    Common fields are inherited from 'users' table.
    """
    __tablename__ = "members"

    # Primary key that references users.id
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    
    # Member-specific fields
    national_id = Column(String(20), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # Member-specific relationships
    subscriptions = relationship("Subscription", back_populates="member", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="member", cascade="all, delete-orphan")
    checkins = relationship("Checkin", back_populates="member", cascade="all, delete-orphan")
    workout_plans = relationship("WorkoutPlan", foreign_keys="[WorkoutPlan.member_id]", cascade="all, delete-orphan")
    waiting_list_entries = relationship("WaitingList", foreign_keys="[WaitingList.member_id]", cascade="all, delete-orphan")

    # Configure polymorphic inheritance
    __mapper_args__ = {
        "polymorphic_identity": "member",
    }

    # Override parent method to demonstrate polymorphism
    def can_login(self) -> bool:
        """
        Members can login only if active and have valid subscription.
        Overrides User.can_login() to add member-specific logic.
        """
        if not self.is_active():
            return False
        # In production, you'd check for active subscription here
        return True

    def has_active_subscription(self) -> bool:
        """Member-specific method to check for active subscriptions."""
        if not self.subscriptions:
            return False
        return any(sub.status == "active" for sub in self.subscriptions)

    def can_check_in(self) -> bool:
        """Member-specific permission check."""
        return self.is_active() and self.has_active_subscription()

    # Override to_dict to include member-specific fields
    def to_dict(self):
        """Extends parent to_dict with member-specific fields."""
        base_dict = super().to_dict()
        base_dict.update({
            "national_id": self.national_id,
        })
        return base_dict
