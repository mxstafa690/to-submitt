from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from services.db import Base


class GymClass(Base):
    __tablename__ = "gym_classes"

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    instructor = Column(String(120), nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=60)
    capacity = Column(Integer, nullable=False, default=20)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    sessions = relationship("Session", back_populates="gym_class", cascade="all, delete-orphan")

    def to_dict(self, include_stats: bool = False):
        data = {
            "id": self.id,
            "title": self.title,
            "instructor": self.instructor,
            "start_time": self.start_time.isoformat(),
            "duration_minutes": self.duration_minutes,
            "capacity": self.capacity,
            "created_at": self.created_at.isoformat(),
        }
        if include_stats:
            active_count = sum(1 for s in self.sessions if s.status == "active")
            canceled_count = sum(1 for s in self.sessions if s.status == "canceled")
            data["stats"] = {
                "active_registrations": active_count,
                "canceled_registrations": canceled_count,
                "available_slots": max(0, self.capacity - active_count),
                "capacity": self.capacity,
            }
        return data
