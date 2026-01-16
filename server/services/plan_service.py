from services.db import get_session
from services.exceptions import NotFoundError, DuplicateError
from models.plan import Plan


class PlanService:
    """Service class for managing plan operations following OOP principles."""

    def __init__(self):
        """Initialize the PlanService."""
        pass

    def list_plans(self):
        """Retrieve all plans ordered by ID."""
        session = get_session()
        try:
            return session.query(Plan).order_by(Plan.id.asc()).all()
        finally:
            session.close()

    def get_plan(self, plan_id: int) -> Plan:
        """Get a specific plan by ID.
        
        Args:
            plan_id: The ID of the plan to retrieve
            
        Returns:
            Plan object
            
        Raises:
            NotFoundError: If plan not found
        """
        session = get_session()
        try:
            plan = session.query(Plan).filter(Plan.id == plan_id).first()
            if not plan:
                raise NotFoundError("Plan not found")
            return plan
        finally:
            session.close()

    def create_plan(self, name: str, type: str, price: float, valid_days: int, max_entries: int | None):
        """Create a new plan.
        
        Args:
            name: Name of the plan
            type: Type of plan (time/entries)
            price: Price of the plan
            valid_days: Number of valid days
            max_entries: Maximum entries (None for unlimited)
            
        Returns:
            Created Plan object
            
        Raises:
            DuplicateError: If plan name already exists
        """
        session = get_session()
        try:
            existing = session.query(Plan).filter(Plan.name == name).first()
            if existing:
                raise DuplicateError("Plan name already exists")

            plan = Plan(
                name=name,
                type=type,
                price=price,
                valid_days=valid_days,
                max_entries=max_entries,
            )
            session.add(plan)
            session.commit()
            session.refresh(plan)
            return plan
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
