from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from services.db import Base


class WaitingList(Base):
    """
    Simple waiting list for gym classes.
    When a class is full, members can join the waiting list.
    """
    __tablename__ = "waiting_lists"

    id = Column(Integer, primary_key=True)
    gym_class_id = Column(Integer, ForeignKey("gym_classes.id"), nullable=False, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    position = Column(Integer, nullable=False)  # Position in queue
    joined_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    gym_class = relationship("GymClass")
    member = relationship("Member")

    def to_dict(self):
        return {
            "id": self.id,
            "gym_class_id": self.gym_class_id,
            "member_id": self.member_id,
            "position": self.position,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
        }
