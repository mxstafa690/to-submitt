"""
Migration script to recreate tables with new User structure (first_name, last_name)
"""
from config.db_config import get_database_uri
from services.db import init_db, engine, Base
from models.user import User
from models.member import Member
from models.trainer import Trainer
from models.admin import Admin
from models.reception import Reception
from models.plan import Plan
from models.subscription import Subscription
from models.gym_class import GymClass
from models.session import Session
from models.workout_plan import WorkoutPlan
from models.workout_item import WorkoutItem
from models.payment import Payment
from models.checkin import Checkin
from models.waiting_list import WaitingList


def migrate():
    """Drop all tables and recreate with new schema"""
    database_uri = get_database_uri()
    init_db(database_uri)
    
    from services.db import engine
    
    print("⚠️  Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("✓ Creating new tables with updated schema...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Migration complete! All tables recreated.")
    print("   Now run seed.py to populate test data.")


if __name__ == "__main__":
    migrate()
