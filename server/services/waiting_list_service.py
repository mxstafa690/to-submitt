from services.db import get_session
from services.exceptions import NotFoundError, DuplicateError
from models.waiting_list import WaitingList
from models.gym_class import GymClass
from models.member import Member


class WaitingListService:
    """Service for managing gym class waiting lists."""

    def __init__(self):
        """Initialize the WaitingListService."""
        pass

    def add_to_waitlist(self, class_id: int, member_id: int) -> WaitingList:
        """Add a member to the waiting list for a class.
        
        Args:
            class_id: The ID of the gym class
            member_id: The ID of the member
            
        Returns:
            Created WaitingList entry
            
        Raises:
            NotFoundError: If class or member not found
            DuplicateError: If member already on waiting list
        """
        session = get_session()
        try:
            # Verify class exists
            gym_class = session.query(GymClass).filter(GymClass.id == class_id).first()
            if not gym_class:
                raise NotFoundError("Class not found")

            # Verify member exists
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                raise NotFoundError("Member not found")

            # Check if already on waiting list
            existing = session.query(WaitingList).filter(
                WaitingList.gym_class_id == class_id,
                WaitingList.member_id == member_id
            ).first()
            if existing:
                raise DuplicateError("Member already on waiting list")

            # Get next position
            max_position = session.query(WaitingList).filter(
                WaitingList.gym_class_id == class_id
            ).count()

            entry = WaitingList(
                gym_class_id=class_id,
                member_id=member_id,
                position=max_position + 1
            )
            session.add(entry)
            session.commit()
            session.refresh(entry)
            return entry
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_waitlist(self, class_id: int):
        """Get all members on waiting list for a class, ordered by position.
        
        Args:
            class_id: The ID of the gym class
            
        Returns:
            List of WaitingList entries
        """
        session = get_session()
        try:
            return session.query(WaitingList).filter(
                WaitingList.gym_class_id == class_id
            ).order_by(WaitingList.position.asc()).all()
        finally:
            session.close()

    def remove_from_waitlist(self, class_id: int, member_id: int):
        """Remove a member from the waiting list.
        
        Args:
            class_id: The ID of the gym class
            member_id: The ID of the member
            
        Raises:
            NotFoundError: If entry not found
        """
        session = get_session()
        try:
            entry = session.query(WaitingList).filter(
                WaitingList.gym_class_id == class_id,
                WaitingList.member_id == member_id
            ).first()
            
            if not entry:
                raise NotFoundError("Waiting list entry not found")

            session.delete(entry)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_next_from_waitlist(self, class_id: int):
        """Get the next member from waiting list (lowest position).
        
        Args:
            class_id: The ID of the gym class
            
        Returns:
            WaitingList entry or None if list is empty
        """
        session = get_session()
        try:
            return session.query(WaitingList).filter(
                WaitingList.gym_class_id == class_id
            ).order_by(WaitingList.position.asc()).first()
        finally:
            session.close()
