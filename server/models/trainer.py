from sqlalchemy import Column, Integer, String, ForeignKey
from models.user import User


class Trainer(User):
    """
    Trainer model using joined-table inheritance from User.
    Trainer-specific data is stored in 'trainers' table.
    Common fields are inherited from 'users' table.
    """
    __tablename__ = "trainers"

    # Primary key that references users.id
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    
    # Trainer-specific fields
    password_hash = Column(String(255), nullable=False)
    specialization = Column(String(100), nullable=True)  # e.g., "Strength", "Cardio", "Yoga"
    certification = Column(String(100), nullable=True)  # e.g., "ACE", "NASM"

    # Configure polymorphic inheritance
    __mapper_args__ = {
        "polymorphic_identity": "trainer",
    }

    # Override parent method to demonstrate polymorphism
    def can_login(self) -> bool:
        """
        Trainers can login if active.
        Overrides User.can_login() with trainer-specific logic.
        """
        return self.is_active()

    def get_display_name(self) -> str:
        """
        Override to show trainer with specialization.
        Demonstrates polymorphism - different behavior than User/Member.
        """
        base = f"{self.get_full_name()} ({self.role.upper()})"
        if self.specialization:
            return f"{base} - {self.specialization}"
        return base

    # Trainer-specific management methods (Polymorphism - shared with Admin)
    def can_manage_classes(self) -> bool:
        """Trainer/Admin permission to manage gym classes."""
        return self.is_active()

    def can_manage_sessions(self) -> bool:
        """Trainer/Admin permission to manage class sessions."""
        return self.is_active()

    def can_manage_workout_plans(self) -> bool:
        """Trainer/Admin permission to manage workout plans."""
        return self.is_active()

    # Override to_dict to include trainer-specific fields
    def to_dict(self):
        """Extends parent to_dict with trainer-specific fields."""
        base_dict = super().to_dict()
        base_dict.update({
            "specialization": self.specialization,
            "certification": self.certification,
        })
        return base_dict
