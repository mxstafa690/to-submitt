from sqlalchemy import Column, Integer, ForeignKey
from models.user import User


class Reception(User):
    """
    Reception model using joined-table inheritance from User.
    Reception-specific data is stored in 'receptions' table.
    Common fields are inherited from 'users' table.
    
    Reception staff handle check-ins and member registrations.
    """
    __tablename__ = "receptions"

    # Primary key that references users.id
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    # Configure polymorphic inheritance
    __mapper_args__ = {
        "polymorphic_identity": "reception",
    }

    def can_check_in(self) -> bool:
        """Reception can check in members."""
        return self.is_active()

    def can_view_checkins(self) -> bool:
        """Reception can view all check-ins."""
        return self.is_active()

    def to_dict(self):
        """Extends parent to_dict with reception-specific fields."""
        base_dict = super().to_dict()
        return base_dict
