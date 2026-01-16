from datetime import datetime, timedelta, date
import pymysql

from config.db_config import get_database_uri
from services.db import init_db, create_all_tables, get_session

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


def create_database_if_not_exists():
    """Create the database if it doesn't exist."""
    import configparser
    import os
    
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
    config.read(config_path)
    
    mysql_config = config['mysql']
    host = mysql_config.get('host', 'localhost')
    port = int(mysql_config.get('port', 3306))
    user = mysql_config.get('user', 'root')
    password = mysql_config.get('password', '')
    database = mysql_config.get('database', 'fittrack')
    
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        connection.commit()
        print(f"✓ Database '{database}' created or already exists")
        cursor.close()
        connection.close()
    except pymysql.Error as e:
        print(f"✗ Error creating database: {e}")
        raise


def run_seed():
    # Create database first
    create_database_if_not_exists()
    
    # Initialize database (read credentials from config.ini)
    database_uri = get_database_uri()
    init_db(database_uri)
    create_all_tables()
    print("✓ Database tables created")

    session = get_session()
    try:
        # -------------------------
        # MEMBERS
        # -------------------------
        if session.query(Member).count() == 0:
            m1 = Member(
                first_name="Dana",
                last_name="Cohen",
                email="dana@example.com",
                phone="0501234567",
                date_of_birth=date(1990, 5, 15),
                national_id="123456789",
                password_hash="Aa1!aaaa",
                status="active",
            )
            m2 = Member(
                first_name="Noam",
                last_name="Cohen",
                email="noam@example.com",
                phone="0521234567",
                date_of_birth=date(1995, 8, 20),
                national_id="987654321",
                password_hash="Bb2!bbbb",
                status="active",
            )
            session.add_all([m1, m2])
            session.commit()

        m1 = session.query(Member).filter(Member.email == "dana@example.com").first()
        m2 = session.query(Member).filter(Member.email == "noam@example.com").first()

        # -------------------------
        # TRAINERS
        # -------------------------
        if session.query(Trainer).count() == 0:
            t1 = Trainer(
                first_name="Sarah",
                last_name="Trainer",
                email="sarah.trainer@fittrack.com",
                phone="0531111111",
                date_of_birth=date(1988, 3, 10),
                password_hash="Cc3!cccc",
                specialization="Strength Training",
                certification="NASM-CPT",
                status="active",
            )
            t2 = Trainer(
                first_name="Mike",
                last_name="Cardio",
                email="mike.cardio@fittrack.com",
                phone="0532222222",
                date_of_birth=date(1992, 7, 25),
                password_hash="Dd4!dddd",
                specialization="Cardio & HIIT",
                certification="ACE-CPT",
                status="active",
            )
            session.add_all([t1, t2])
            session.commit()

        # -------------------------
        # ADMINS
        # -------------------------
        if session.query(Admin).count() == 0:
            a1 = Admin(
                first_name="System",
                last_name="Admin",
                email="admin@fittrack.com",
                phone="0543333333",
                date_of_birth=date(1985, 1, 1),
                password_hash="Ee5!eeee",
                specialization="Management",
                certification="Admin",
                access_level="full",
                status="active",
            )
            a2 = Admin(
                first_name="Manager",
                last_name="User",
                email="manager@fittrack.com",
                phone="0544444444",
                date_of_birth=date(1990, 6, 12),
                password_hash="Ff6!ffff",
                specialization="Support",
                certification="Admin",
                access_level="limited",
                status="active",
            )
            session.add_all([a1, a2])
            session.commit()

        # -------------------------
        # RECEPTION
        # -------------------------
        if session.query(Reception).count() == 0:
            r1 = Reception(
                first_name="Front",
                last_name="Desk",
                email="reception@fittrack.com",
                phone="0545555555",
                date_of_birth=date(1998, 4, 8),
                status="active",
            )
            session.add(r1)
            session.commit()

        # -------------------------
        # PLANS
        # -------------------------
        if session.query(Plan).count() == 0:
            p1 = Plan(
                name="Monthly",
                type="time",
                price=199,
                valid_days=30,
                max_entries=None,
            )
            p2 = Plan(
                name="Annual",
                type="time",
                price=1990,
                valid_days=365,
                max_entries=None,
            )
            session.add_all([p1, p2])
            session.commit()

        p1 = session.query(Plan).filter(Plan.name == "Monthly").first()
        p2 = session.query(Plan).filter(Plan.name == "Annual").first()

        # -------------------------
        # SUBSCRIPTIONS
        # -------------------------
        if session.query(Subscription).count() == 0 and m1 and m2 and p1 and p2:
            start = date.today()
            s1 = Subscription(
                member_id=m1.id,
                plan_id=p1.id,
                status="active",
                start_date=start,
                end_date=start + timedelta(days=p1.valid_days),
                remaining_entries=p1.max_entries,
            )
            s2 = Subscription(
                member_id=m2.id,
                plan_id=p2.id,
                status="active",
                start_date=start,
                end_date=start + timedelta(days=p2.valid_days),
                remaining_entries=p2.max_entries,
            )
            session.add_all([s1, s2])
            session.commit()

        # -------------------------
        # CLASSES
        # -------------------------
        if session.query(GymClass).count() == 0:
            gc1 = GymClass(
                title="Morning Strength",
                instructor="Dana Trainer",
                start_time=datetime.now() + timedelta(days=1),
                duration_minutes=60,
                capacity=20,
            )
            gc2 = GymClass(
                title="Evening Cardio",
                instructor="Noam Trainer",
                start_time=datetime.now() + timedelta(days=2),
                duration_minutes=45,
                capacity=25,
            )
            session.add_all([gc1, gc2])
            session.commit()

        gc1 = session.query(GymClass).filter(GymClass.title == "Morning Strength").first()
        gc2 = session.query(GymClass).filter(GymClass.title == "Evening Cardio").first()

        # -------------------------
        # SESSIONS (Bookings)
        # -------------------------
        if session.query(Session).count() == 0 and gc1 and gc2 and m1 and m2:
            se1 = Session(
                gym_class_id=gc1.id,
                member_id=m1.id,
                status="booked",
                attended=False,
            )
            se2 = Session(
                gym_class_id=gc2.id,
                member_id=m2.id,
                status="booked",
                attended=False,
            )
            session.add_all([se1, se2])
            session.commit()

        # -------------------------
        # WORKOUT PLANS
        # -------------------------
        if session.query(WorkoutPlan).count() == 0 and m1 and m2:
            wp1 = WorkoutPlan(
                member_id=m1.id,
                trainer_name="Coach Dana",
                title="Strength - Beginner",
                is_active=True,
            )
            wp2 = WorkoutPlan(
                member_id=m2.id,
                trainer_name="Coach Noam",
                title="Cardio - Beginner",
                is_active=True,
            )
            session.add_all([wp1, wp2])
            session.commit()

        wp1 = session.query(WorkoutPlan).filter(WorkoutPlan.title == "Strength - Beginner").first()
        wp2 = session.query(WorkoutPlan).filter(WorkoutPlan.title == "Cardio - Beginner").first()

        # -------------------------
        # WORKOUT ITEMS
        # -------------------------
        if session.query(WorkoutItem).count() == 0 and wp1 and wp2:
            wi1 = WorkoutItem(
                plan_id=wp1.id,
                exercise_name="Deadlift",
                sets=4,
                reps=5,
                target_weight=80.0,
                notes="TEST NOTE",
            )
            wi2 = WorkoutItem(
                plan_id=wp2.id,
                exercise_name="Running",
                sets=1,
                reps=1,
                target_weight=0.0,
                notes="20 minutes easy pace",
            )
            session.add_all([wi1, wi2])
            session.commit()

        # -------------------------
        # PAYMENTS
        # -------------------------
        s1 = session.query(Subscription).filter(Subscription.member_id == m1.id).first() if m1 else None
        s2 = session.query(Subscription).filter(Subscription.member_id == m2.id).first() if m2 else None

        if session.query(Payment).count() == 0 and s1 and s2:
            pay1 = Payment(
                subscription_id=s1.id,
                amount=199.0,
                status="completed",
                reference="PAY-001",
                paid_at=datetime.utcnow(),
            )
            pay2 = Payment(
                subscription_id=s2.id,
                amount=1990.0,
                status="completed",
                reference="PAY-002",
                paid_at=datetime.utcnow(),
            )
            pay3 = Payment(
                subscription_id=s1.id,
                amount=199.0,
                status="pending",
                reference="PAY-003",
                paid_at=None,
            )
            session.add_all([pay1, pay2, pay3])
            session.commit()

        # -------------------------
        # CHECKINS
        # -------------------------
        if session.query(Checkin).count() == 0 and m1 and m2:
            ch1 = Checkin(member_id=m1.id, result="approved", reason=None)
            ch2 = Checkin(member_id=m2.id, result="approved", reason=None)
            ch3 = Checkin(member_id=m1.id, result="denied", reason="Subscription expired")
            session.add_all([ch1, ch2, ch3])
            session.commit()

        # Display results
        print("\n" + "="*70)
        print("✅ DATABASE SEEDED SUCCESSFULLY!")
        print("="*70)
        
        print("\n📋 CREATED USERS - Use these IDs in Postman:")
        print("-"*70)
        
        all_users = session.query(User).all()
        for user in all_users:
            print(f"  ID: {user.id:2d} | Role: {user.role:10s} | Email: {user.email}")
        
        print("\n" + "="*70)
        print("🔑 TEST CREDENTIALS FOR POSTMAN:")
        print("="*70)
        print("  Member (dana):          ID=1  | Password: Aa1!aaaa")
        print("  Member (noam):          ID=2  | Password: Bb2!bbbb")
        print("  Trainer (sarah):        ID=3  | Password: Cc3!cccc")
        print("  Trainer (mike):         ID=4  | Password: Dd4!dddd")
        print("  Admin (full access):    ID=5  | Password: Ee5!eeee")
        print("  Admin (limited access): ID=6  | Password: Ff6!ffff")
        print("  Reception (staff):      ID=7  | No password")
        print("="*70)
        
        print("\n📊 DATABASE STATISTICS:")
        print("-"*70)
        print(f"  Members:        {session.query(Member).count()}")
        print(f"  Trainers:       {session.query(Trainer).count()}")
        print(f"  Admins:         {session.query(Admin).count()}")
        print(f"  Reception:      {session.query(Reception).count()}")
        print(f"  Plans:          {session.query(Plan).count()}")
        print(f"  Subscriptions:  {session.query(Subscription).count()}")
        print(f"  Gym Classes:    {session.query(GymClass).count()}")
        print(f"  Sessions:       {session.query(Session).count()}")
        print(f"  Workout Plans:  {session.query(WorkoutPlan).count()}")
        print(f"  Workout Items:  {session.query(WorkoutItem).count()}")
        print(f"  Payments:       {session.query(Payment).count()}")
        print(f"  Check-ins:      {session.query(Checkin).count()}")
        print("="*70 + "\n")

    except Exception as e:
        session.rollback()
        print(f"Error during seed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run_seed()
