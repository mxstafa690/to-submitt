from datetime import date, timedelta
from services.db import get_session
from services.exceptions import NotFoundError, DuplicateError
from models.member import Member
from models.plan import Plan
from models.subscription import Subscription
from config.constants import DEFAULT_SUBSCRIPTION_STATUS, SubscriptionStatus


class SubscriptionService:
    """Service class for managing subscription operations following OOP principles."""

    def __init__(self):
        """Initialize the SubscriptionService."""
        pass

    def list_member_subscriptions(self, member_id: int):
        """List all subscriptions for a specific member.
        
        Args:
            member_id: The ID of the member
            
        Returns:
            List of Subscription objects
            
        Raises:
            NotFoundError: If member not found
        """
        session = get_session()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                raise NotFoundError("Member not found")
            return session.query(Subscription).filter(Subscription.member_id == member_id).order_by(Subscription.id.asc()).all()
        finally:
            session.close()

    def get_subscription(self, subscription_id: int):
        """Get a specific subscription by ID.
        
        Args:
            subscription_id: The ID of the subscription
            
        Returns:
            Subscription object
            
        Raises:
            NotFoundError: If subscription not found
        """
        session = get_session()
        try:
            sub = session.query(Subscription).filter(Subscription.id == subscription_id).first()
            if not sub:
                raise NotFoundError("Subscription not found")
            return sub
        finally:
            session.close()

    def create_subscription(self, member_id: int, plan_id: int, start_date_value: date | None = None):
        """Create a new subscription for a member.
        
        Args:
            member_id: The ID of the member
            plan_id: The ID of the plan
            start_date_value: Optional start date (defaults to today)
            
        Returns:
            Created Subscription object
            
        Raises:
            NotFoundError: If member or plan not found
            DuplicateError: If member already has an active subscription
        """
        session = get_session()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                raise NotFoundError("Member not found")

            plan = session.query(Plan).filter(Plan.id == plan_id).first()
            if not plan:
                raise NotFoundError("Plan not found")

            active_existing = (
                session.query(Subscription)
                .filter(Subscription.member_id == member_id)
                .order_by(Subscription.id.desc())
                .first()
            )
            if active_existing:
                active_existing.recompute_status()
                if active_existing.status in (SubscriptionStatus.ACTIVE.value, SubscriptionStatus.FROZEN.value):
                    raise DuplicateError("Member already has an active subscription")

            start_date_value = start_date_value or date.today()
            end_date_value = start_date_value + timedelta(days=int(plan.valid_days))
            remaining_entries = int(plan.max_entries) if plan.max_entries is not None else None

            sub = Subscription(
                member_id=member_id,
                plan_id=plan_id,
                status=DEFAULT_SUBSCRIPTION_STATUS.value,
                start_date=start_date_value,
                end_date=end_date_value,
                remaining_entries=remaining_entries,
                frozen_until=None,
            )
            session.add(sub)
            session.commit()
            session.refresh(sub)
            return sub
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def freeze_subscription(self, subscription_id: int, days: int):
        """Freeze a subscription for a specified number of days.
        
        Args:
            subscription_id: The ID of the subscription
            days: Number of days to freeze
            
        Returns:
            Updated Subscription object
        """
        session = get_session()
        try:
            sub = session.query(Subscription).filter(Subscription.id == subscription_id).first()
            if not sub:
                raise NotFoundError("Subscription not found")
                
            today = date.today()
            sub.frozen_until = today + timedelta(days=days)
            sub.status = SubscriptionStatus.FROZEN.value
            session.commit()
            session.refresh(sub)
            return sub
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def unfreeze_subscription(self, subscription_id: int):
        """Unfreeze a subscription.
        
        Args:
            subscription_id: The ID of the subscription
            
        Returns:
            Updated Subscription object
        """
        session = get_session()
        try:
            sub = session.query(Subscription).filter(Subscription.id == subscription_id).first()
            if not sub:
                raise NotFoundError("Subscription not found")
                
            sub.frozen_until = None
            sub.status = SubscriptionStatus.ACTIVE.value
            session.commit()
            session.refresh(sub)
            return sub
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_subscription(self, subscription_id: int):
        """Delete a subscription.
        
        Args:
            subscription_id: The ID of the subscription
            
        Raises:
            NotFoundError: If subscription not found
        """
        session = get_session()
        try:
            sub = session.query(Subscription).filter(Subscription.id == subscription_id).first()
            if not sub:
                raise NotFoundError("Subscription not found")
            
            session.delete(sub)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def subscription_status_for_member(self, member_id: int):
        """Get subscription status for a member.
        
        Args:
            member_id: The ID of the member
            
        Returns:
            Dictionary with subscription status information
        """
        subs = self.list_member_subscriptions(member_id)
        if not subs:
            return {"member_id": member_id, "has_subscription": False, "status": "none"}

        sub = subs[-1]
        sub.recompute_status()

        today = date.today()
        days_left = (sub.end_date - today).days
        if days_left < 0:
            days_left = 0

        return {
            "member_id": member_id,
            "has_subscription": True,
            "subscription_id": sub.id,
            "status": sub.status,
            "days_left": days_left,
            "remaining_entries": sub.remaining_entries,
            "frozen_until": sub.frozen_until.isoformat() if sub.frozen_until else None,
            "plan_id": sub.plan_id,
        }
