# full_reset_migration.py - Complete database reset and setup
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database_models import Base, User, Client, Schedule, VisitLog
from app.database2 import DATABASE_URL, hash_password
from datetime import datetime
import uuid
import sys


def full_reset_migration():
    """Complete database reset with fresh unified tables and sample data"""

    print("🚨 WARNING: This will COMPLETELY DELETE your existing database!")
    print("🚨 All data will be lost and replaced with fresh sample data.")
    response = input("Type 'RESET' to confirm: ")

    if response != "RESET":
        print("❌ Migration cancelled")
        return

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)

    try:
        with SessionLocal() as db:
            print("🗑️ Step 1: Dropping all existing tables...")

            # Drop entire schema and recreate (nuclear option)
            db.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
            db.execute(text("CREATE SCHEMA public"))
            db.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
            db.execute(text("GRANT ALL ON SCHEMA public TO public"))
            db.commit()

            print("✅ All old tables deleted")
            print("🏗️ Step 2: Creating fresh unified table structure...")

            # Create all new tables
            Base.metadata.create_all(bind=engine)
            print("✅ New unified tables created")

            print("👥 Step 3: Creating sample users...")

            # Create admin
            admin = User(
                email="admin@carehome.com",
                password_hash=hash_password("admin123"),
                role="admin"
            )
            db.add(admin)

            # Create managers
            managers = [
                User(
                    email="dr.smith@carehome.com",
                    password_hash=hash_password("manager123"),
                    role="manager",
                    name="Dr. Amanda Smith",
                    department="Medical Director"
                ),
                User(
                    email="nurse.supervisor@carehome.com",
                    password_hash=hash_password("manager456"),
                    role="manager",
                    name="Jennifer Taylor",
                    department="Nursing Supervisor"
                ),
                User(
                    email="admin.head@carehome.com",
                    password_hash=hash_password("manager789"),
                    role="manager",
                    name="Robert Chen",
                    department="Administration"
                )
            ]

            for manager in managers:
                db.add(manager)

            # Create carers
            carers = [
                User(
                    email="sarah.jones@carehome.com",
                    password_hash=hash_password("carer123"),
                    role="carer",
                    name="Sarah Jones",
                    phone="447987654321"
                ),
                User(
                    email="mike.wilson@carehome.com",
                    password_hash=hash_password("carer456"),
                    role="carer",
                    name="Mike Wilson",
                    phone="447555123456"
                ),
                User(
                    email="emma.brown@carehome.com",
                    password_hash=hash_password("carer789"),
                    role="carer",
                    name="Emma Brown",
                    phone="447666789123"
                ),
                User(
                    email="alex.taylor@carehome.com",
                    password_hash=hash_password("carer999"),
                    role="carer",
                    name="Alex Taylor",
                    phone="447123987654"
                ),
                User(
                    email="lisa.white@carehome.com",
                    password_hash=hash_password("carer555"),
                    role="carer",
                    name="Lisa White",
                    phone="447888999000"
                )
            ]

            for carer in carers:
                db.add(carer)

            # Create family members
            families = [
                User(
                    email="mary.johnson@gmail.com",
                    password_hash=hash_password("family123"),
                    role="family",
                    name="Mary Johnson",
                    phone="447111222333",
                    family_id="F001"
                ),
                User(
                    email="david.davis@outlook.com",
                    password_hash=hash_password("family456"),
                    role="family",
                    name="David Davis",
                    phone="447444555666",
                    family_id="F002"
                ),
                User(
                    email="linda.thompson@yahoo.com",
                    password_hash=hash_password("family789"),
                    role="family",
                    name="Linda Thompson",
                    phone="447777888999",
                    family_id="F003"
                ),
                User(
                    email="susan.miller@gmail.com",
                    password_hash=hash_password("family321"),
                    role="family",
                    name="Susan Miller",
                    phone="447222333444",
                    family_id="F004"
                ),
                User(
                    email="james.wilson@hotmail.com",
                    password_hash=hash_password("family654"),
                    role="family",
                    name="James Wilson Jr",
                    phone="447555666777",
                    family_id="F005"
                )
            ]

            for family in families:
                db.add(family)

            print("🏠 Step 4: Creating sample clients...")

            # Create clients with realistic care needs
            clients = [
                Client(
                    id="C001",
                    name="Robert Johnson",
                    age=78,
                    room="101A",
                    date_of_birth="1946-03-15",
                    support_needs="Personal care assistance, mobility support, medication reminders. Requires assistance with daily activities and personal care routines."
                ),
                Client(
                    id="C002",
                    name="Margaret Davis",
                    age=82,
                    room="102B",
                    date_of_birth="1942-07-22",
                    support_needs="Memory support, mobility assistance, fall prevention. Needs supervision and gentle encouragement for daily activities."
                ),
                Client(
                    id="C003",
                    name="William Thompson",
                    age=75,
                    room="103A",
                    date_of_birth="1949-11-08",
                    support_needs="Respiratory support, mobility assistance, emotional support. Requires breathing support equipment and limited mobility assistance."
                ),
                Client(
                    id="C004",
                    name="Dorothy Miller",
                    age=88,
                    room="201C",
                    date_of_birth="1936-01-30",
                    support_needs="Memory support, mobility assistance, personal care. Requires full assistance with personal care and gentle reassurance."
                ),
                Client(
                    id="C005",
                    name="Charles Wilson",
                    age=71,
                    room="202A",
                    date_of_birth="1953-09-12",
                    support_needs="Movement support, swallowing assistance. Requires modified diet and movement support care."
                ),
                Client(
                    id="C006",
                    name="Betty Anderson",
                    age=79,
                    room="203B",
                    date_of_birth="1945-05-18",
                    support_needs="Recovery support, left side weakness, communication assistance. Movement therapy ongoing."
                ),
                Client(
                    id="C007",
                    name="Frank Martinez",
                    age=84,
                    room="204A",
                    date_of_birth="1940-12-03",
                    support_needs="Kidney support care, dietary assistance, vision support. Special care routine 3x weekly."
                ),
                Client(
                    id="C008",
                    name="Helen Garcia",
                    age=76,
                    room="205C",
                    date_of_birth="1948-04-25",
                    support_needs="Recovery support, anxiety management, comfort care. Comfort management care plan in place."
                )
            ]

            for client in clients:
                db.add(client)

            # Commit users and clients before creating relationships
            db.commit()

            print("🔗 Step 5: Creating user-client assignments...")

            # Create assignments using raw SQL for simplicity
            assignments_data = [
                # Sarah Jones -> C001, C002
                ("sarah.jones@carehome.com", "C001"),
                ("sarah.jones@carehome.com", "C002"),
                # Mike Wilson -> C003, C004
                ("mike.wilson@carehome.com", "C003"),
                ("mike.wilson@carehome.com", "C004"),
                # Emma Brown -> C005, C006
                ("emma.brown@carehome.com", "C005"),
                ("emma.brown@carehome.com", "C006"),
                # Alex Taylor -> C007
                ("alex.taylor@carehome.com", "C007"),
                # Lisa White -> C008
                ("lisa.white@carehome.com", "C008"),
                # Family assignments
                ("mary.johnson@gmail.com", "C001"),
                ("david.davis@outlook.com", "C002"),
                ("linda.thompson@yahoo.com", "C003"),
                ("susan.miller@gmail.com", "C004"),
                ("james.wilson@hotmail.com", "C005")
            ]

            for user_email, client_id in assignments_data:
                db.execute(text(
                    "INSERT INTO assignments (user_email, client_id) VALUES (:email, :client_id)"
                ), {"email": user_email, "client_id": client_id})

            print("📅 Step 6: Creating sample schedules...")

            # Create schedules for today and tomorrow
            today = datetime.now().date().strftime("%Y-%m-%d")
            tomorrow = datetime.now().date().replace(day=datetime.now().day + 1).strftime("%Y-%m-%d")

            schedules = [
                # Today's schedules
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="sarah.jones@carehome.com",
                    client_id="C001",
                    date=today,
                    start_time="08:00",
                    end_time="11:00",
                    shift_type="morning",
                    status="completed",
                    notes="Regular morning care routine - completed successfully"
                ),
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="mike.wilson@carehome.com",
                    client_id="C003",
                    date=today,
                    start_time="09:00",
                    end_time="12:00",
                    shift_type="morning",
                    status="in_progress",
                    notes="Respiratory support session ongoing"
                ),
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="emma.brown@carehome.com",
                    client_id="C005",
                    date=today,
                    start_time="14:00",
                    end_time="17:00",
                    shift_type="afternoon",
                    status="scheduled",
                    notes="Movement therapy and personal care"
                ),
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="alex.taylor@carehome.com",
                    client_id="C007",
                    date=today,
                    start_time="16:00",
                    end_time="19:00",
                    shift_type="evening",
                    status="scheduled",
                    notes="Evening care and medication support"
                ),
                # Tomorrow's schedules
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="sarah.jones@carehome.com",
                    client_id="C002",
                    date=tomorrow,
                    start_time="08:30",
                    end_time="11:30",
                    shift_type="morning",
                    status="scheduled",
                    notes="Memory support and mobility assistance"
                ),
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="lisa.white@carehome.com",
                    client_id="C008",
                    date=tomorrow,
                    start_time="10:00",
                    end_time="13:00",
                    shift_type="morning",
                    status="scheduled",
                    notes="Anxiety management and comfort care"
                )
            ]

            for schedule in schedules:
                db.add(schedule)

            print("📝 Step 7: Creating sample visit logs...")

            # Create sample visit logs
            visit_logs = [
                VisitLog(
                    id=f"VL{str(uuid.uuid4())[:8].upper()}",
                    client_id="C001",
                    carer_name="Sarah Jones",
                    carer_number="447987654321",
                    date=datetime.now(),
                    personal_care_completed=True,
                    care_reminders_provided="Morning medication reminders provided as requested, all care preferences followed",
                    toilet=True,
                    changed_clothes=True,
                    ate_food="Enjoyed full breakfast, dietary preferences accommodated",
                    notes="Client in good spirits today. All care routines completed successfully. Mobility exercises done.",
                    mood=["happy", "cooperative"]
                ),
                VisitLog(
                    id=f"VL{str(uuid.uuid4())[:8].upper()}",
                    client_id="C002",
                    carer_name="Sarah Jones",
                    carer_number="447987654321",
                    date=datetime.now(),
                    personal_care_completed=True,
                    care_reminders_provided="Memory support provided, daily routine reinforced",
                    toilet=True,
                    changed_clothes=True,
                    ate_food="Assisted with lunch, ate well with encouragement",
                    notes="Better orientation today. Client remembered carer's name and enjoyed conversation about her past.",
                    mood=["alert", "nostalgic"]
                ),
                VisitLog(
                    id=f"VL{str(uuid.uuid4())[:8].upper()}",
                    client_id="C003",
                    carer_name="Mike Wilson",
                    carer_number="447555123456",
                    date=datetime.now(),
                    personal_care_completed=False,
                    care_reminders_provided="Breathing support equipment checked and functioning well",
                    toilet=True,
                    changed_clothes=True,
                    ate_food="Small portions due to breathing comfort, appetite maintained",
                    notes="Respiratory therapy session completed. Client positioned comfortably. Movement exercises adapted for breathing.",
                    mood=["determined", "comfortable"]
                )
            ]

            for visit_log in visit_logs:
                db.add(visit_log)

            # Final commit
            db.commit()

            print("🎉 Migration completed successfully!")
            print("\n" + "=" * 60)
            print("✅ FRESH DATABASE SETUP COMPLETE")
            print("=" * 60)
            print("\n👥 TEST USERS CREATED:")
            print("  🔑 Admin:     admin@carehome.com / admin123")
            print("  👔 Manager:   dr.smith@carehome.com / manager123")
            print("  👩‍⚕️ Carer:     sarah.jones@carehome.com / carer123")
            print("  👨‍👩‍👧‍👦 Family:    mary.johnson@gmail.com / family123")
            print("\n📊 SAMPLE DATA CREATED:")
            print(f"  • {len(managers) + len(carers) + len(families) + 1} Users (unified table)")
            print(f"  • {len(clients)} Clients")
            print(f"  • {len(assignments_data)} User-Client assignments")
            print(f"  • {len(schedules)} Schedules (today & tomorrow)")
            print(f"  • {len(visit_logs)} Visit logs")
            print("\n🏗️ DATABASE ARCHITECTURE:")
            print("  ✅ Single 'users' table with role column")
            print("  ✅ Single 'assignments' table for relationships")
            print("  ✅ Clean foreign key relationships")
            print("  ✅ No bloated/complex tables")
            print("\n🚀 SYSTEM READY FOR:")
            print("  ✅ Care home deployment testing")
            print("  ✅ Microsoft internship interviews")
            print("  ✅ Production-level reliability")
            print("\n" + "=" * 60)

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    full_reset_migration()