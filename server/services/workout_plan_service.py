from services.db import get_session
from services.exceptions import NotFoundError, FitTrackError, ForbiddenError
from models.member import Member
from models.trainer import Trainer
from models.workout_plan import WorkoutPlan
from models.workout_item import WorkoutItem


class WorkoutPlanService:
    """Service class for managing workout plan operations following OOP principles."""

    def __init__(self):
        """Initialize the WorkoutPlanService."""
        pass

    def create_workout_plan(self, data: dict, trainer_id: int | None = None) -> WorkoutPlan:
        """Create a new workout plan with items.
        
        Demonstrates OOP: Uses Trainer.can_manage_workout_plans() to validate permissions.
        
        Args:
            data: Dictionary containing plan and items data
            trainer_id: ID of trainer creating the plan (for OOP permission check)
            
        Returns:
            Created WorkoutPlan object
            
        Raises:
            FitTrackError: If required fields are missing
            NotFoundError: If member not found
            ForbiddenError: If trainer doesn't have permission
        """
        member_id = data.get("member_id")
        title = data.get("title")
        trainer_name = data.get("trainer_name")
        items = data.get("items", [])

        if not member_id or not title or not trainer_name:
            raise FitTrackError("member_id, title, trainer_name are required")

        session = get_session()
        try:
            # USE OOP METHOD: Trainer.can_manage_workout_plans() checks permissions
            if trainer_id:
                trainer = session.query(Trainer).filter(Trainer.id == trainer_id).first()
                if trainer and not trainer.can_manage_workout_plans():
                    raise ForbiddenError(
                        f"Trainer '{trainer.get_display_name()}' is not authorized to manage workout plans. "
                        "Status must be 'active'."
                    )
            
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                raise NotFoundError("Member not found")

            plan = WorkoutPlan(member_id=member_id, title=title, trainer_name=trainer_name)
            session.add(plan)
            session.flush()

            for it in items:
                exercise_name = it.get("exercise_name")
                sets = it.get("sets")
                reps = it.get("reps")

                if not exercise_name or sets is None or reps is None:
                    raise FitTrackError("Each item requires exercise_name, sets, reps")

                item = WorkoutItem(
                    plan_id=plan.id,
                    exercise_name=exercise_name,
                    sets=sets,
                    reps=reps,
                    target_weight=it.get("target_weight"),
                    notes=it.get("notes"),
                )
                session.add(item)

            session.commit()
            session.refresh(plan)
            return plan
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def list_workout_plans_for_member(self, member_id: int) -> list[WorkoutPlan]:
        """List all workout plans for a member.
        
        Args:
            member_id: The ID of the member
            
        Returns:
            List of WorkoutPlan objects
            
        Raises:
            NotFoundError: If member not found
        """
        session = get_session()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                raise NotFoundError("Member not found")

            return (
                session.query(WorkoutPlan)
                .filter(WorkoutPlan.member_id == member_id)
                .order_by(WorkoutPlan.created_at.desc())
                .all()
            )
        finally:
            session.close()

    def get_active_workout_plan_for_member(self, member_id: int) -> WorkoutPlan | None:
        """Get the active workout plan for a member.
        
        Args:
            member_id: The ID of the member
            
        Returns:
            Active WorkoutPlan object or None
            
        Raises:
            NotFoundError: If member not found
        """
        session = get_session()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                raise NotFoundError("Member not found")

            return (
                session.query(WorkoutPlan)
                .filter(WorkoutPlan.member_id == member_id, WorkoutPlan.is_active == True)
                .order_by(WorkoutPlan.created_at.desc())
                .first()
            )
        finally:
            session.close()

    def set_workout_plan_active(self, plan_id: int, is_active: bool) -> WorkoutPlan:
        """Set a workout plan's active status.
        
        Args:
            plan_id: The ID of the workout plan
            is_active: Whether the plan should be active
            
        Returns:
            Updated WorkoutPlan object
            
        Raises:
            NotFoundError: If workout plan not found
        """
        session = get_session()
        try:
            plan = session.query(WorkoutPlan).filter(WorkoutPlan.id == plan_id).first()
            if not plan:
                raise NotFoundError("Workout plan not found")

            plan.is_active = bool(is_active)
            session.commit()
            session.refresh(plan)
            return plan
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def list_workout_plan_items(self, plan_id: int) -> list[WorkoutItem]:
        """List all items in a workout plan.
        
        Args:
            plan_id: The ID of the workout plan
            
        Returns:
            List of WorkoutItem objects
            
        Raises:
            NotFoundError: If workout plan not found
        """
        session = get_session()
        try:
            plan = session.query(WorkoutPlan).filter(WorkoutPlan.id == plan_id).first()
            if not plan:
                raise NotFoundError("Workout plan not found")

            return (
                session.query(WorkoutItem)
                .filter(WorkoutItem.plan_id == plan_id)
                .order_by(WorkoutItem.id.asc())
                .all()
            )
        finally:
            session.close()

    def get_workout_item(self, item_id: int) -> WorkoutItem:
        """Get a specific workout item.
        
        Args:
            item_id: The ID of the workout item
            
        Returns:
            WorkoutItem object
            
        Raises:
            NotFoundError: If workout item not found
        """
        session = get_session()
        try:
            item = session.query(WorkoutItem).filter(WorkoutItem.id == item_id).first()
            if not item:
                raise NotFoundError("Workout item not found")
            return item
        finally:
            session.close()

    def update_workout_item(self, item_id: int, data: dict) -> WorkoutItem:
        """Update a workout item.
        
        Args:
            item_id: The ID of the workout item
            data: Dictionary with fields to update
            
        Returns:
            Updated WorkoutItem object
            
        Raises:
            NotFoundError: If workout item not found
        """
        session = get_session()
        try:
            item = session.query(WorkoutItem).filter(WorkoutItem.id == item_id).first()
            if not item:
                raise NotFoundError("Workout item not found")

            allowed = {"exercise_name", "sets", "reps", "target_weight", "notes"}
            for k, v in data.items():
                if k in allowed:
                    setattr(item, k, v)

            session.commit()
            session.refresh(item)
            return item
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_workout_item(self, item_id: int) -> bool:
        """Delete a workout item.
        
        Args:
            item_id: The ID of the workout item
            
        Returns:
            True if deleted successfully
            
        Raises:
            NotFoundError: If workout item not found
        """
        session = get_session()
        try:
            item = session.query(WorkoutItem).filter(WorkoutItem.id == item_id).first()
            if not item:
                raise NotFoundError("Workout item not found")

            session.delete(item)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    # Aliases for backward compatibility
    def list_member_workout_plans(self, member_id: int) -> list[WorkoutPlan]:
        """Alias for list_workout_plans_for_member."""
        return self.list_workout_plans_for_member(member_id)

    def get_member_active_workout_plan(self, member_id: int) -> WorkoutPlan | None:
        """Alias for get_active_workout_plan_for_member."""
        return self.get_active_workout_plan_for_member(member_id)

    def get_workout_plan_items(self, plan_id: int) -> list[WorkoutItem]:
        """Alias for list_workout_plan_items."""
        return self.list_workout_plan_items(plan_id)
