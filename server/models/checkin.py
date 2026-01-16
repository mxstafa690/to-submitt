from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from services.db import Base


class Checkin(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True)

    member_id = Column(
        Integer,
        ForeignKey("members.id"),
        nullable=False,
        index=True,
    )

    result = Column(String(20), nullable=False)  # approved / denied
    reason = Column(String(255), nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    member = relationship("Member")

    def to_dict(self):
        return {
            "id": self.id,
            "member_id": self.member_id,
            "result": self.result,
            "reason": self.reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
