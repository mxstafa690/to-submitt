from sqlalchemy import Column, Integer, String, Float
from models.base import BaseModel


class WorkoutItem(BaseModel):
    __tablename__ = "workout_items"

    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, nullable=False, index=True)
    exercise_name = Column(String(255), nullable=False)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    target_weight = Column(Float, nullable=True)
    notes = Column(String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "exercise_name": self.exercise_name,
            "sets": self.sets,
            "reps": self.reps,
            "target_weight": float(self.target_weight) if self.target_weight is not None else None,
            "notes": self.notes,
        }
