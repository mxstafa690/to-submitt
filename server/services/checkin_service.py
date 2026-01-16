from datetime import datetime, date

from services.db import get_session
from services.exceptions import NotFoundError

from models.member import Member
from models.subscription import Subscription
from models.checkin import Checkin
from models.payment import Payment


class CheckinService:
    """Service class for managing checkin operations following OOP principles."""

    def __init__(self):
        """Initialize the CheckinService."""
        pass

    def _today(self) -> date:
        """Get current date."""
        return datetime.utcnow().date()

    def _get_latest_subscription_for_member(self, member_id: int, session) -> Subscription | None:
        """מחזיר את המנוי האחרון של המתאמן (אם יש).
        לא מסננים לפי status כדי שנוכל להחזיר סיבה נכונה (expired/frozen/canceled).
        """
        return (
            session.query(Subscription)
            .filter(Subscription.member_id == member_id)
            .order_by(Subscription.id.desc())
            .first()
        )

    def checkin_member(self, member_id: int) -> Checkin:
        """Check-in a member using OOP method Member.can_check_in().
        
        This demonstrates polymorphism - the Member object determines if check-in is allowed
        based on its status and subscription state.
        
        Returns:
            Checkin object with result='approved' or 'denied' and appropriate reason
        """
        session = get_session()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                raise NotFoundError("Member not found")

            # DEBT VALIDATION: Check for pending/unpaid payments before allowing check-in
            pending_payments = session.query(Payment).join(Subscription).filter(
                Subscription.member_id == member_id,
                Payment.status.in_(["pending", "canceled"])
            ).count()
            
            if pending_payments > 0:
                checkin = Checkin(
                    member_id=member_id, 
                    result="denied", 
                    reason="Pending payment exists. Please settle outstanding debts."
                )
                session.add(checkin)
                session.commit()
                session.refresh(checkin)
                return checkin

            # USE OOP METHOD: Member.can_check_in() encapsulates all business rules
            # This demonstrates inheritance and polymorphism in action
            if not member.can_check_in():
                # Determine specific reason for denial
                if not member.is_active():
                    reason = "Member account is not active"
                elif not member.has_active_subscription():
                    reason = "No active subscription found"
                else:
                    reason = "Check-in not allowed"
                
                checkin = Checkin(member_id=member_id, result="denied", reason=reason)
                session.add(checkin)
                session.commit()
                session.refresh(checkin)
                return checkin

            # Member can check in - now validate subscription details
            sub = self._get_latest_subscription_for_member(member_id, session)
            today = self._today()

            if not sub:
                checkin = Checkin(member_id=member_id, result="denied", reason="No subscription")
                session.add(checkin)
                session.commit()
                session.refresh(checkin)
                return checkin

            # Check if subscription is canceled
            if getattr(sub, "status", None) == "canceled":
                checkin = Checkin(member_id=member_id, result="denied", reason="Subscription canceled")
                session.add(checkin)
                session.commit()
                session.refresh(checkin)
                return checkin

            # תוקף תאריכים
            if sub.start_date and sub.start_date > today:
                checkin = Checkin(member_id=member_id, result="denied", reason="Subscription not started yet")
                session.add(checkin)
                session.commit()
                session.refresh(checkin)
                return checkin

            if sub.end_date and sub.end_date < today:
                checkin = Checkin(member_id=member_id, result="denied", reason="Subscription expired")
                session.add(checkin)
                session.commit()
                session.refresh(checkin)
                return checkin

            # קפוא
            if sub.frozen_until and sub.frozen_until >= today:
                checkin = Checkin(member_id=member_id, result="denied", reason="Subscription is frozen")
                session.add(checkin)
                session.commit()
                session.refresh(checkin)
                return checkin

            # כרטיסייה
            if sub.remaining_entries is not None:
                if sub.remaining_entries <= 0:
                    checkin = Checkin(member_id=member_id, result="denied", reason="No remaining entries")
                    session.add(checkin)
                    session.commit()
                    session.refresh(checkin)
                    return checkin

                sub.remaining_entries -= 1

            checkin = Checkin(member_id=member_id, result="approved", reason="OK")
            session.add(checkin)
            session.commit()
            session.refresh(checkin)
            return checkin
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def list_checkins(self, member_id: int | None = None):
        """List all checkins, optionally filtered by member.
        
        Args:
            member_id: Optional member ID to filter by
            
        Returns:
            List of Checkin objects
        """
        session = get_session()
        try:
            q = session.query(Checkin).order_by(Checkin.id.desc())
            if member_id is not None:
                q = q.filter(Checkin.member_id == member_id)
            return q.all()
        finally:
            session.close()
