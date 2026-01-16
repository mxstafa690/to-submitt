from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime
from services.db import Base

"""
abstact class that initiates tables with two main feilds
"""
class BaseModel(Base):
    """Base model with id and created_at."""
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

#still dont know what the real use of this is ???????
    def base_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
