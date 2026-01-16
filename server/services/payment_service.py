from datetime import datetime
from services.db import get_session
from services.exceptions import NotFoundError
from models.subscription import Subscription
from models.payment import Payment
from config.constants import DEFAULT_PAYMENT_STATUS, PaymentStatus


class PaymentService:
    """Service class for managing payment operations following OOP principles."""

    def __init__(self):
        """Initialize the PaymentService."""
        pass

    def list_payments(self, subscription_id: int | None = None):
        """List all payments, optionally filtered by subscription.
        
        Args:
            subscription_id: Optional subscription ID to filter by
            
        Returns:
            List of Payment objects
        """
        session = get_session()
        try:
            q = session.query(Payment).order_by(Payment.id.asc())
            if subscription_id is not None:
                q = q.filter(Payment.subscription_id == subscription_id)
            return q.all()
        finally:
            session.close()

    def get_payment(self, payment_id: int):
        """Get a specific payment by ID.
        
        Args:
            payment_id: The ID of the payment
            
        Returns:
            Payment object
            
        Raises:
            NotFoundError: If payment not found
        """
        session = get_session()
        try:
            payment = session.query(Payment).filter(Payment.id == payment_id).first()
            if not payment:
                raise NotFoundError("Payment not found")
            return payment
        finally:
            session.close()

    def create_payment(self, subscription_id: int, amount: float, reference: str | None = None):
        """Create a new payment.
        
        Args:
            subscription_id: The ID of the subscription
            amount: Payment amount
            reference: Optional payment reference
            
        Returns:
            Created Payment object
            
        Raises:
            NotFoundError: If subscription not found
        """
        session = get_session()
        try:
            sub = session.query(Subscription).filter(Subscription.id == subscription_id).first()
            if not sub:
                raise NotFoundError("Subscription not found")

            payment = Payment(
                subscription_id=subscription_id,
                amount=amount,
                status=DEFAULT_PAYMENT_STATUS.value,
                reference=reference,
            )
            session.add(payment)
            session.commit()
            session.refresh(payment)
            return payment
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def update_payment_status(self, payment_id: int, status: str):
        """Update payment status.
        
        Args:
            payment_id: The ID of the payment
            status: New status (pending/paid/canceled)
            
        Returns:
            Updated Payment object
        """
        session = get_session()
        try:
            payment = session.query(Payment).filter(Payment.id == payment_id).first()
            if not payment:
                raise NotFoundError("Payment not found")
                
            payment.status = status

            # If marking as paid — record paid_at timestamp
            if status == PaymentStatus.PAID.value and payment.paid_at is None:
                payment.paid_at = datetime.utcnow()

            # If returning to pending/canceled — clear paid_at
            if status in (PaymentStatus.PENDING.value, PaymentStatus.CANCELED.value):
                payment.paid_at = None

            session.commit()
            session.refresh(payment)
            return payment
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
