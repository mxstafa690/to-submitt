from sqlalchemy import Column, Integer, String, ForeignKey
from models.trainer import Trainer


class Admin(Trainer):
    """
    Admin model using joined-table inheritance from Trainer.
    Admin-specific data is stored in 'admins' table.
    Trainer fields are inherited from 'trainers' table.
    User fields are inherited from 'users' table.
    
    Admin inherits all Trainer capabilities (manage classes, sessions, workout plans)
    and adds additional admin-specific capabilities (manage members, finances).
    Demonstrates multi-level polymorphic inheritance.
    """
    __tablename__ = "admins"

    # Primary key that references trainers.id
    id = Column(Integer, ForeignKey("trainers.id"), primary_key=True)
    
    # Admin-specific fields
    access_level = Column(String(50), nullable=False, default="limited")  # "full", "limited", "readonly"

    # Configure polymorphic inheritance
    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

    def get_display_name(self) -> str:
        """
        Override to show admin with access level.
        Demonstrates polymorphism - different behavior than User/Member/Trainer.
        """
        return f"{self.get_full_name()} ({self.role.upper()}: {self.access_level.upper()})"

    # Admin-specific methods (in addition to inherited Trainer methods)
    def has_full_access(self) -> bool:
        """Check if admin has full system access."""
        return self.is_active() and self.access_level == "full"

    def can_manage_members(self) -> bool:
        """Admin-specific permission to manage members."""
        return self.is_active() and self.access_level in ["full", "limited"]

    def can_manage_finances(self) -> bool:
        """Admin-specific permission to manage payments and finances."""
        return self.has_full_access()

    def can_manage_subscription_plans(self) -> bool:
        """Admin-specific permission to manage subscription plans (memberships)."""
        return self.is_active() and self.access_level in ["full", "limited"]

    # Override can_manage_* methods to require full access for admin
    def can_manage_classes(self) -> bool:
        """Admin permission to manage gym classes - requires full access."""
        return self.has_full_access()

    def can_manage_sessions(self) -> bool:
        """Admin permission to manage class sessions - requires full access."""
        return self.has_full_access()

    def can_manage_workout_plans(self) -> bool:
        """Admin permission to manage workout plans - requires full access."""
        return self.has_full_access()

    # Override to_dict to include admin-specific fields
    def to_dict(self):
        """Extends trainer to_dict with admin-specific fields."""
        base_dict = super().to_dict()
        base_dict.update({
            "access_level": self.access_level,
        })
        return base_dict
