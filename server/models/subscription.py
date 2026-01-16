from datetime import datetime, date, timedelta
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from services.db import Base
from config.constants import DEFAULT_SUBSCRIPTION_STATUS, SubscriptionStatus


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False, index=True)

    status = Column(String(20), nullable=False, default=DEFAULT_SUBSCRIPTION_STATUS.value)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    remaining_entries = Column(Integer, nullable=True)
    frozen_until = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    member = relationship("Member", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
    payments = relationship("Payment", foreign_keys="[Payment.subscription_id]", cascade="all, delete-orphan")

    def recompute_status(self, today: date | None = None):
        today = today or date.today()
        if self.frozen_until and self.frozen_until >= today:
            self.status = SubscriptionStatus.FROZEN.value
            return self.status
        if self.end_date < today:
            self.status = SubscriptionStatus.EXPIRED.value
            return self.status
        if self.status not in (SubscriptionStatus.CANCELED.value,):
            self.status = SubscriptionStatus.ACTIVE.value
        return self.status

    def to_dict(self):
        self.recompute_status()
        return {
            "id": self.id,
            "member_id": self.member_id,
            "plan_id": self.plan_id,
            "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "remaining_entries": self.remaining_entries,
            "frozen_until": self.frozen_until.isoformat() if self.frozen_until else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
