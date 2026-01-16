from models.gym_class import GymClass
from models.trainer import Trainer
from services.db import get_session
from services.exceptions import NotFoundError, ForbiddenError


class ClassService:
    """Service class for managing gym class operations following OOP principles."""

    def __init__(self):
        """Initialize the ClassService."""
        pass

    def create_class(self, title: str, instructor: str, start_time, duration_minutes: int, capacity: int, trainer_id: int | None = None) -> GymClass:
        """Create a new gym class.
        
        Demonstrates OOP: Uses Trainer.can_manage_classes() to validate permissions.
        
        Args:
            title: Title of the class
            instructor: Instructor name
            start_time: Start time of the class
            duration_minutes: Duration in minutes
            capacity: Maximum capacity
            trainer_id: ID of trainer creating the class (optional for admins)
            
        Returns:
            Created GymClass object
            
        Raises:
            ForbiddenError: If trainer doesn't have permission to manage classes
        """
        session = get_session()
        try:
            # USE OOP METHOD: Trainer.can_manage_classes() checks permissions
            if trainer_id:
                trainer = session.query(Trainer).filter(Trainer.id == trainer_id).first()
                if trainer and not trainer.can_manage_classes():
                    raise ForbiddenError(
                        f"Trainer '{trainer.get_display_name()}' is not authorized to manage classes. "
                        "Status must be 'active'."
                    )
            
            gym_class = GymClass(
                title=title,
                instructor=instructor,
                start_time=start_time,
                duration_minutes=duration_minutes,
                capacity=capacity,
            )
            session.add(gym_class)
            session.commit()
            session.refresh(gym_class)
            return gym_class
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def list_classes(self):
        """List all gym classes ordered by start time.
        
        Returns:
            List of GymClass objects
        """
        session = get_session()
        try:
            return session.query(GymClass).order_by(GymClass.start_time.asc()).all()
        finally:
            session.close()

    def get_class(self, class_id: int) -> GymClass:
        """Get a specific gym class by ID.
        
        Args:
            class_id: The ID of the gym class
            
        Returns:
            GymClass object
            
        Raises:
            NotFoundError: If class not found
        """
        session = get_session()
        try:
            gym_class = session.query(GymClass).filter(GymClass.id == class_id).first()
            if not gym_class:
                raise NotFoundError("Class not found")
            return gym_class
        finally:
            session.close()
