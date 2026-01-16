from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from services.db import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    gym_class_id = Column(Integer, ForeignKey("gym_classes.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)

    status = Column(String(20), nullable=False, default="active")
    attended = Column(Boolean, nullable=False, default=False)
    registered_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    gym_class = relationship("GymClass", back_populates="sessions")
    member = relationship("Member", back_populates="sessions")

    def to_dict(self):
        return {
            "id": self.id,
            "gym_class_id": self.gym_class_id,
            "member_id": self.member_id,
            "status": self.status,
            "attended": self.attended,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
