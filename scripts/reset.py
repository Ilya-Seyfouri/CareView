# scripts/reset_db.py - CareView Database Reset Script
"""
Database reset script for CareView care home management system.
Creates fresh database with sample data for development and testing.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database_models import Base, User, Client, Schedule, VisitLog
from app.database import DATABASE_URL, hash_password
from datetime import datetime, timedelta
import uuid
import sys


def reset_database():
    """Complete database reset with sample care home data"""

    print("🚨 WARNING: This will COMPLETELY DELETE your existing database!")
    print("🚨 All data will be lost and replaced with sample data.")
    response = input("Type 'RESET' to confirm: ")

    if response != "RESET":
        print("❌ Reset cancelled")
        return

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)

    try:
        with SessionLocal() as db:
            print("🗑️ Step 1: Dropping all existing tables...")
            Base.metadata.drop_all(bind=engine)
            print("✅ All old tables deleted")

            print("🏗️ Step 2: Creating fresh table structure...")
            Base.metadata.create_all(bind=engine)
            print("✅ New tables created")

            print("👥 Step 3: Creating sample users...")

            users = [
                # Managers
                User(
                    email="manager@demo.com",
                    password_hash=hash_password("password123"),
                    role="manager",
                    name="Sarah Harrison",
                    department="Care Management"
                ),
                User(
                    email="admin@demo.com",
                    password_hash=hash_password("password123"),
                    role="admin"
                ),

                # Care Staff
                User(
                    email="carer@demo.com",
                    password_hash=hash_password("password123"),
                    role="carer",
                    name="Emily Watson",
                    phone="01234567890"
                ),
                User(
                    email="carer2@demo.com",
                    password_hash=hash_password("password123"),
                    role="carer",
                    name="Michael Johnson",
                    phone="01234567891"
                ),
                User(
                    email="carer3@demo.com",
                    password_hash=hash_password("password123"),
                    role="carer",
                    name="Lisa Chen",
                    phone="01234567892"
                ),

                # Family Members
                User(
                    email="family@demo.com",
                    password_hash=hash_password("password123"),
                    role="family",
                    name="John Smith",
                    phone="01234567893",
                    family_id="FAM001"
                ),
                User(
                    email="family2@demo.com",
                    password_hash=hash_password("password123"),
                    role="family",
                    name="Mary Jones",
                    phone="01234567894",
                    family_id="FAM002"
                )
            ]

            for user in users:
                db.add(user)

            print("🏠 Step 4: Creating sample clients...")

            clients = [
                Client(
                    id="CL001",
                    name="Robert Wilson",
                    age=78,
                    room="101A",
                    date_of_birth="1946-03-15",
                    support_needs="Mobility assistance, medication reminders twice daily. Enjoys reading and music. Family visits on weekends."
                ),
                Client(
                    id="CL002",
                    name="Margaret Thompson",
                    age=82,
                    room="102B",
                    date_of_birth="1942-07-22",
                    support_needs="Dementia care, requires gentle encouragement with meals. Likes looking at photo albums and listening to classical music."
                ),
                Client(
                    id="CL003",
                    name="James Brown",
                    age=75,
                    room="103A",
                    date_of_birth="1949-11-08",
                    support_needs="Diabetes management, regular blood sugar checks. Independent with personal care. Enjoys watching football."
                ),
                Client(
                    id="CL004",
                    name="Dorothy Davis",
                    age=79,
                    date_of_birth="1943-09-12",
                    room="104B",
                    support_needs="Post-stroke care, assistance with left side mobility. Speech therapy exercises. Loves gardening activities."
                ),
                Client(
                    id="CL005",
                    name="William Miller",
                    age=79,
                    room="105A",
                    date_of_birth="1945-01-30",
                    support_needs="Heart condition monitoring, limited exertion. Medication management. Enjoys chess and card games."
                )
            ]

            for client in clients:
                db.add(client)

            # Commit users and clients before creating relationships
            db.commit()

            print("🔗 Step 5: Creating care assignments...")

            # Create assignments
            assignments_data = [
                # Emily Watson -> Robert and Margaret
                ("carer@demo.com", "CL001"),
                ("carer@demo.com", "CL002"),
                # Michael Johnson -> James and Dorothy
                ("carer2@demo.com", "CL003"),
                ("carer2@demo.com", "CL004"),
                # Lisa Chen -> William
                ("carer3@demo.com", "CL005"),
                # Family assignments
                ("family@demo.com", "CL001"),
                ("family2@demo.com", "CL002")
            ]

            for user_email, client_id in assignments_data:
                db.execute(text(
                    "INSERT INTO assignments (user_email, client_id) VALUES (:email, :client_id)"
                ), {"email": user_email, "client_id": client_id})

            print("📅 Step 6: Creating sample schedules...")

            # Create schedules for today and upcoming days
            today = datetime.now().date()
            tomorrow = today + timedelta(days=1)
            day_after = today + timedelta(days=2)

            schedules = [
                # Today's schedules
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="carer@demo.com",
                    client_id="CL001",
                    date=today.strftime("%Y-%m-%d"),
                    start_time="09:00",
                    end_time="10:30",
                    shift_type="morning",
                    status="completed",
                    notes="Morning care completed successfully"
                ),
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="carer2@demo.com",
                    client_id="CL003",
                    date=today.strftime("%Y-%m-%d"),
                    start_time="11:00",
                    end_time="12:00",
                    shift_type="morning",
                    status="in_progress",
                    notes="Diabetes monitoring and medication"
                ),
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="carer3@demo.com",
                    client_id="CL005",
                    date=today.strftime("%Y-%m-%d"),
                    start_time="14:00",
                    end_time="15:30",
                    shift_type="afternoon",
                    status="scheduled",
                    notes="Heart condition check and activities"
                ),

                # Tomorrow's schedules
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="carer@demo.com",
                    client_id="CL002",
                    date=tomorrow.strftime("%Y-%m-%d"),
                    start_time="08:30",
                    end_time="10:00",
                    shift_type="morning",
                    status="scheduled",
                    notes="Dementia care and breakfast assistance"
                ),
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="carer2@demo.com",
                    client_id="CL004",
                    date=tomorrow.strftime("%Y-%m-%d"),
                    start_time="10:30",
                    end_time="12:00",
                    shift_type="morning",
                    status="scheduled",
                    notes="Post-stroke physiotherapy session"
                )
            ]

            for schedule in schedules:
                db.add(schedule)

            print("📝 Step 7: Creating sample visit logs...")

            # Create sample visit logs
            visit_logs = [
                VisitLog(
                    id=f"VL{str(uuid.uuid4())[:8].upper()}",
                    client_id="CL001",
                    carer_name="Emily Watson",
                    carer_number="01234567890",
                    date=datetime.now(),
                    personal_care_completed=True,
                    care_reminders_provided="Morning medication taken, mobility exercises completed",
                    toilet=True,
                    changed_clothes=True,
                    ate_food="Full breakfast consumed including porridge and tea",
                    notes="Robert was in excellent spirits today. Enjoyed our chat about his garden. Mobility seems improved from yesterday.",
                    mood=["happy", "chatty", "comfortable"]
                ),
                VisitLog(
                    id=f"VL{str(uuid.uuid4())[:8].upper()}",
                    client_id="CL002",
                    carer_name="Emily Watson",
                    carer_number="01234567890",
                    date=datetime.now() - timedelta(hours=2),
                    personal_care_completed=True,
                    care_reminders_provided="Gentle encouragement with breakfast, photo album activity",
                    toilet=True,
                    changed_clothes=True,
                    ate_food="Half portion breakfast, encouraged to finish orange juice",
                    notes="Margaret was a bit confused this morning but responded well to music. Family photos helped her settle.",
                    mood=["confused", "calmer", "responsive"]
                )
            ]

            for visit_log in visit_logs:
                db.add(visit_log)

            # Final commit
            db.commit()

            print("🎉 Database reset completed successfully!")
            print("\n" + "=" * 60)
            print("✅ CAREVIEW DATABASE READY")
            print("=" * 60)
            print("\n👥 DEMO ACCOUNTS CREATED:")
            print("  🔑 Admin:    admin@demo.com / password123")
            print("  👔 Manager:  manager@demo.com / password123")
            print("  👩‍⚕️ Carer:    carer@demo.com / password123")
            print("  👨‍👩‍👧‍👦 Family:   family@demo.com / password123")
            print("\n📊 SAMPLE DATA CREATED:")
            print(f"  • {len(users)} Users")
            print(f"  • {len(clients)} Clients")
            print(f"  • {len(assignments_data)} Care assignments")
            print(f"  • {len(schedules)} Schedules")
            print(f"  • {len(visit_logs)} Visit logs")
            print("\n🚀 SYSTEM READY FOR:")
            print("  ✅ Development and testing")
            print("  ✅ API demonstrations")
            print("  ✅ Technical interviews")
            print("\n🌐 ACCESS POINTS:")
            print("  • API: http://localhost:8000")
            print("  • Docs: http://localhost:8000/docs")
            print("  • Health: http://localhost:8000/health")
            print("\n" + "=" * 60)

    except Exception as e:
        print(f"❌ Database reset failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    reset_database()