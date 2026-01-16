from datetime import datetime
from models.session import Session
from models.member import Member
from services.db import get_session
from services.exceptions import NotFoundError, DuplicateError
from services.class_service import ClassService


class SessionService:
    """Service class for managing session operations following OOP principles."""

    def __init__(self):
        """Initialize the SessionService."""
        self.class_service = ClassService()

    def register_member_to_class(self, class_id: int, member_id: int) -> Session:
        """Register a member to a gym class.
        
        Args:
            class_id: The ID of the gym class
            member_id: The ID of the member
            
        Returns:
            Created or updated Session object
            
        Raises:
            NotFoundError: If class or member not found
            DuplicateError: If member already registered or class is full
        """
        gym_class = self.class_service.get_class(class_id)
        
        session = get_session()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                raise NotFoundError("Member not found")

            existing = session.query(Session).filter(
                Session.gym_class_id == class_id,
                Session.member_id == member_id
            ).first()
            if existing and existing.status == "active":
                raise DuplicateError("Member already registered")

            active_count = session.query(Session).filter(
                Session.gym_class_id == class_id,
                Session.status == "active"
            ).count()
            if active_count >= gym_class.capacity:
                raise DuplicateError("Class is full")

            if existing and existing.status == "canceled":
                existing.status = "active"
                existing.canceled_at = None
                existing.registered_at = datetime.utcnow()
                session.commit()
                session.refresh(existing)
                return existing

            s = Session(gym_class_id=class_id, member_id=member_id, status="active")
            session.add(s)
            session.commit()
            session.refresh(s)
            return s
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def cancel_registration(self, class_id: int, member_id: int) -> Session:
        """Cancel a member's registration to a gym class.
        
        Args:
            class_id: The ID of the gym class
            member_id: The ID of the member
            
        Returns:
            Updated Session object
            
        Raises:
            NotFoundError: If registration not found
        """
        session = get_session()
        try:
            s = session.query(Session).filter(
                Session.gym_class_id == class_id,
                Session.member_id == member_id
            ).first()
            if not s:
                raise NotFoundError("Registration not found")

            if s.status == "canceled":
                return s

            s.status = "canceled"
            s.canceled_at = datetime.utcnow()
            session.commit()
            session.refresh(s)
            return s
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_participants(self, class_id: int):
        """Get all active participants in a gym class.
        
        Args:
            class_id: The ID of the gym class
            
        Returns:
            List of Member objects
        """
        self.class_service.get_class(class_id)
        
        session = get_session()
        try:
            sessions = session.query(Session).filter(
                Session.gym_class_id == class_id,
                Session.status == "active"
            ).all()
            return [s.member for s in sessions]
        finally:
            session.close()

    def get_class_stats(self, class_id: int):
        """Get statistics for a gym class.
        
        Args:
            class_id: The ID of the gym class
            
        Returns:
            Dictionary with class statistics
        """
        gym_class = self.class_service.get_class(class_id)
        
        session = get_session()
        try:
            active_count = session.query(Session).filter(
                Session.gym_class_id == class_id,
                Session.status == "active"
            ).count()
            canceled_count = session.query(Session).filter(
                Session.gym_class_id == class_id,
                Session.status == "canceled"
            ).count()
            return {
                "class_id": class_id,
                "capacity": gym_class.capacity,
                "active_registrations": active_count,
                "canceled_registrations": canceled_count,
                "available_slots": max(0, gym_class.capacity - active_count),
            }
        finally:
            session.close()
