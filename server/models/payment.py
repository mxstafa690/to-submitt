from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from services.db import Base
from config.constants import DEFAULT_PAYMENT_STATUS


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)

    subscription_id = Column(
        Integer,
        ForeignKey("subscriptions.id"),
        nullable=False,
        index=True,
    )

    amount = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default=DEFAULT_PAYMENT_STATUS.value)

    reference = Column(String(120), nullable=True)  # Reference/transaction number
    paid_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # קשר חד־כיווני: Payment -> Subscription
    subscription = relationship("Subscription")

    def to_dict(self):
        return {
            "id": self.id,
            "subscription_id": self.subscription_id,
            "amount": self.amount,
            "status": self.status,
            "reference": self.reference,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
