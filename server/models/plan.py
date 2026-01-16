from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship
from services.db import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False, unique=True)
    type = Column(String(30), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    valid_days = Column(Integer, nullable=False)
    max_entries = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    subscriptions = relationship("Subscription", back_populates="plan", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "price": float(self.price),
            "valid_days": self.valid_days,
            "max_entries": self.max_entries,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
