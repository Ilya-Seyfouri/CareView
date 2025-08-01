# reset.py - Enhanced CareView Database Reset Script
"""
Comprehensive database reset script for CareView care home management system.
Creates realistic demo data perfect for showcasing all features.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database_models import Base, User, Client, Schedule, VisitLog, AuditLog
from app.database import DATABASE_URL, hash_password
from datetime import datetime, timedelta
import uuid
import random


def reset_database():

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)

    try:
        with SessionLocal() as db:
            Base.metadata.drop_all(bind=engine)
            print("All old tables deleted")

            Base.metadata.create_all(bind=engine)
            print("New tables created")

            print("Step 3: Creating user accounts")

            users = [
                # Admin
                User(
                    email="admin@carehome.com",
                    password_hash=hash_password("admin123"),
                    role="admin",
                    name="System Administrator"
                ),

                # Management Team
                User(
                    email="manager@carehome.com",
                    password_hash=hash_password("manager123"),
                    role="manager",
                    name="Sarah Harrison",
                    department="Care Management"
                ),
                User(
                    email="headmanager@carehome.com",
                    password_hash=hash_password("manager123"),
                    role="manager",
                    name="David Thompson",
                    department="Operations"
                ),
                User(
                    email="nightmanager@carehome.com",
                    password_hash=hash_password("manager123"),
                    role="manager",
                    name="Rachel Green",
                    department="Night Operations"
                ),

                # Senior Care Staff
                User(
                    email="emily.watson@carehome.com",
                    password_hash=hash_password("carer123"),
                    role="carer",
                    name="Emily Watson",
                    phone="01234 567 890"
                ),
                User(
                    email="michael.johnson@carehome.com",
                    password_hash=hash_password("carer123"),
                    role="carer",
                    name="Michael Johnson",
                    phone="01234 567 891"
                ),
                User(
                    email="lisa.chen@carehome.com",
                    password_hash=hash_password("carer123"),
                    role="carer",
                    name="Lisa Chen",
                    phone="01234 567 892"
                ),
                User(
                    email="james.brown@carehome.com",
                    password_hash=hash_password("carer123"),
                    role="carer",
                    name="James Brown",
                    phone="01234 567 893"
                ),
                User(
                    email="anna.williams@carehome.com",
                    password_hash=hash_password("carer123"),
                    role="carer",
                    name="Anna Williams",
                    phone="01234 567 894"
                ),

                # Family Members
                User(
                    email="john.smith@family.com",
                    password_hash=hash_password("family123"),
                    role="family",
                    name="John Smith",
                    phone="07700 123 456",
                    family_id="FAM001"
                ),
                User(
                    email="mary.jones@family.com",
                    password_hash=hash_password("family123"),
                    role="family",
                    name="Mary Jones",
                    phone="07700 123 457",
                    family_id="FAM002"
                ),
                User(
                    email="peter.wilson@family.com",
                    password_hash=hash_password("family123"),
                    role="family",
                    name="Peter Wilson",
                    phone="07700 123 458",
                    family_id="FAM003"
                ),
                User(
                    email="susan.davis@family.com",
                    password_hash=hash_password("family123"),
                    role="family",
                    name="Susan Davis",
                    phone="07700 123 459",
                    family_id="FAM004"
                ),

                # Demo Accounts
                User(
                    email="admin@demo.com",
                    password_hash=hash_password("password123"),
                    role="admin",
                    name="Demo Admin"
                ),
                User(
                    email="manager@demo.com",
                    password_hash=hash_password("password123"),
                    role="manager",
                    name="Demo Manager",
                    department="Demo Department"
                ),
                User(
                    email="carer@demo.com",
                    password_hash=hash_password("password123"),
                    role="carer",
                    name="Demo Carer",
                    phone="01234 567 999"
                ),
                User(
                    email="family@demo.com",
                    password_hash=hash_password("password123"),
                    role="family",
                    name="Demo Family",
                    phone="07700 123 999",
                    family_id="FAM999"
                )
            ]

            for user in users:
                db.add(user)

            print(" Step 4: Creating family member profiles")

            clients = [
                Client(
                    id="CL001",
                    name="Robert Wilson",
                    age=78,
                    room="101A",
                    date_of_birth="1946-03-15",
                    support_needs="Advanced dementia care. Requires assistance with all daily activities. Enjoys music therapy and gentle hand massage. Family visits regularly on weekends. Prefers routine and familiar faces."
                ),
                Client(
                    id="CL002",
                    name="Margaret Thompson",
                    age=82,
                    room="102B",
                    date_of_birth="1942-07-22",
                    support_needs="Moderate dementia with sundowning. Independent with eating but needs encouragement. Loves looking at family photos and listening to 1960s music. Can become agitated in the evenings."
                ),
                Client(
                    id="CL003",
                    name="James Patterson",
                    age=75,
                    room="103A",
                    date_of_birth="1949-11-08",
                    support_needs="Type 2 diabetes requiring 4x daily blood glucose monitoring. Insulin dependent. Mobility issues with left leg. Enjoys reading newspapers and discussing current events."
                ),
                Client(
                    id="CL004",
                    name="Dorothy Davis",
                    age=79,
                    date_of_birth="1945-09-12",
                    room="104B",
                    support_needs="Post-stroke rehabilitation. Right-side weakness requiring mobility assistance. Speech therapy exercises twice weekly. Passionate about gardening and bird watching."
                ),
                Client(
                    id="CL005",
                    name="William Miller",
                    age=81,
                    room="105A",
                    date_of_birth="1943-01-30",
                    support_needs="Congestive heart failure. Requires daily weight monitoring and fluid restriction. Oxygen therapy at night. Former teacher who enjoys chess and helping other residents."
                ),
                Client(
                    id="CL006",
                    name="Elizabeth Brown",
                    age=77,
                    room="106B",
                    date_of_birth="1947-06-18",
                    support_needs="Parkinson's disease with tremors and balance issues. Requires assistance with fine motor tasks. Medication timing is critical. Loves classical music and poetry readings."
                ),
                Client(
                    id="CL007",
                    name="Thomas Anderson",
                    age=84,
                    room="107A",
                    date_of_birth="1940-12-03",
                    support_needs="Mild cognitive impairment. Generally independent but needs reminders for medications. Former engineer who enjoys building puzzles and mechanical projects."
                ),
                Client(
                    id="CL008",
                    name="Helen Carter",
                    age=76,
                    room="108B",
                    date_of_birth="1948-04-25",
                    support_needs="Chronic pain management from arthritis. Uses wheelchair for longer distances. Very social and organizes resident activities. Requires pain medication management."
                ),
                Client(
                    id="CL009",
                    name="George Williams",
                    age=80,
                    room="109A",
                    date_of_birth="1944-08-14",
                    support_needs="Recent hip replacement recovery. Physical therapy 3x weekly. Former military officer who appreciates routine and order. Enjoys war documentaries and memoirs."
                ),
                Client(
                    id="CL010",
                    name="Betty Taylor",
                    age="83",
                    room="110B",
                    date_of_birth="1941-02-08",
                    support_needs="Advanced macular degeneration - legally blind. Requires assistance with navigation and reading. Exceptional hearing and memory. Loves audiobooks and music."
                )
            ]

            for client in clients:
                db.add(client)

            # Commit users and clients before creating relationships
            db.commit()

            print("Step 5: Creating care assignments")

            assignments_data = [
                # Emily Watson  - 3 clients
                ("emily.watson@carehome.com", "CL001"),
                ("emily.watson@carehome.com", "CL002"),
                ("emily.watson@carehome.com", "CL003"),

                # Michael Johnson - 2 clients
                ("michael.johnson@carehome.com", "CL004"),
                ("michael.johnson@carehome.com", "CL005"),

                # Lisa Chen - 3 clients
                ("lisa.chen@carehome.com", "CL006"),
                ("lisa.chen@carehome.com", "CL007"),
                ("lisa.chen@carehome.com", "CL008"),

                # James Brown - 2 clients
                ("james.brown@carehome.com", "CL009"),
                ("james.brown@carehome.com", "CL010"),

                # Anna Williams
                ("anna.williams@carehome.com", "CL001"),
                ("anna.williams@carehome.com", "CL005"),

                # Carer assignments
                ("carer@demo.com", "CL001"),
                ("carer@demo.com", "CL002"),

                # Family assignments
                ("john.smith@family.com", "CL001"),
                ("mary.jones@family.com", "CL002"),
                ("peter.wilson@family.com", "CL003"),
                ("susan.davis@family.com", "CL004"),
                ("family@demo.com", "CL001"),
            ]

            for user_email, client_id in assignments_data:
                db.execute(text(
                    "INSERT INTO assignments (user_email, client_id) VALUES (:email, :client_id)"
                ), {"email": user_email, "client_id": client_id})

            print("Step 6: Creating schedule data")

            schedules = []
            today = datetime.now().date()

            # Past week schedules (completed)
            for days_ago in range(7, 0, -1):
                date = today - timedelta(days=days_ago)
                schedules.extend([
                    Schedule(
                        id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                        carer_email="emily.watson@carehome.com",
                        client_id="CL001",
                        date=date.strftime("%Y-%m-%d"),
                        start_time="09:00",
                        end_time="10:30",
                        shift_type="morning",
                        status="completed",
                        notes="Morning dementia care completed successfully"
                    ),
                    Schedule(
                        id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                        carer_email="michael.johnson@carehome.com",
                        client_id="CL004",
                        date=date.strftime("%Y-%m-%d"),
                        start_time="14:00",
                        end_time="15:30",
                        shift_type="afternoon",
                        status="completed",
                        notes="Post-stroke physiotherapy and mobility exercises"
                    )
                ])

            # Todays schedules (mixed)
            schedules.extend([
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="emily.watson@carehome.com",
                    client_id="CL001",
                    date=today.strftime("%Y-%m-%d"),
                    start_time="08:30",
                    end_time="10:00",
                    shift_type="morning",
                    status="completed",
                    notes="Morning routine and medication administration"
                ),
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="lisa.chen@carehome.com",
                    client_id="CL006",
                    date=today.strftime("%Y-%m-%d"),
                    start_time="11:00",
                    end_time="12:30",
                    shift_type="morning",
                    status="in_progress",
                    notes="Parkinson's care and tremor management"
                ),
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="james.brown@carehome.com",
                    client_id="CL009",
                    date=today.strftime("%Y-%m-%d"),
                    start_time="15:00",
                    end_time="16:30",
                    shift_type="afternoon",
                    status="scheduled",
                    notes="Hip replacement recovery exercises"
                ),
                Schedule(
                    id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                    carer_email="carer@demo.com",
                    client_id="CL001",
                    date=today.strftime("%Y-%m-%d"),
                    start_time="19:00",
                    end_time="20:00",
                    shift_type="evening",
                    status="scheduled",
                    notes="Evening care and bedtime routine"
                )
            ])

            # Future schedules
            for days_ahead in range(1, 8):
                date = today + timedelta(days=days_ahead)
                schedules.extend([
                    Schedule(
                        id=f"SCH{str(uuid.uuid4())[:8].upper()}",
                        carer_email=random.choice([
                            "emily.watson@carehome.com",
                            "michael.johnson@carehome.com",
                            "lisa.chen@carehome.com"
                        ]),
                        client_id=random.choice(["CL001", "CL002", "CL003", "CL004", "CL005"]),
                        date=date.strftime("%Y-%m-%d"),
                        start_time=random.choice(["09:00", "14:00", "19:00"]),
                        end_time=random.choice(["10:30", "15:30", "20:30"]),
                        shift_type=random.choice(["morning", "afternoon", "evening"]),
                        status="scheduled",
                        notes="Routine care visit scheduled"
                    )
                ])

            for schedule in schedules:
                db.add(schedule)

            print("Step 7: Creating visit logs")

            visit_logs = []

            visit_scenarios = [
                {
                    "client_id": "CL001",
                    "carer": "Emily Watson",
                    "phone": "01234 567 890",
                    "care_completed": True,
                    "reminders": "Administered morning medications including donepezil. Gentle encouragement with breakfast routine.",
                    "toilet": True,
                    "changed_clothes": True,
                    "food": "Full breakfast consumed - porridge with honey, tea with 2 sugars. Ate well today.",
                    "notes": "Robert was in excellent spirits. Recognized me immediately and asked about my weekend. Mobility stable, no falls. Family photo session helped with reminiscence.",
                    "mood": ["happy", "alert", "cooperative"]
                },
                {
                    "client_id": "CL002",
                    "carer": "Emily Watson",
                    "phone": "01234 567 890",
                    "care_completed": True,
                    "reminders": "Gentle encouragement needed with personal hygiene. Music therapy during care routine.",
                    "toilet": True,
                    "changed_clothes": True,
                    "food": "Partial breakfast - encouraged to finish orange juice. Prefers finger foods.",
                    "notes": "Margaret showed some confusion this morning but responded well to familiar songs from the 1960s. Agitation reduced when shown family photos.",
                    "mood": ["confused", "calmer after music", "responsive to photos"]
                },
                {
                    "client_id": "CL003",
                    "carer": "Michael Johnson",
                    "phone": "01234 567 891",
                    "care_completed": True,
                    "reminders": "Blood glucose check: 8.2 mmol/L (target range). Insulin administered as prescribed.",
                    "toilet": True,
                    "changed_clothes": False,
                    "food": "Diabetic breakfast - controlled carbohydrates. Discussed newspaper headlines during meal.",
                    "notes": "James is managing his diabetes well. Enjoyed discussion about local football results. Left leg mobility slightly improved from yesterday.",
                    "mood": ["cheerful", "engaged", "independent"]
                },
                {
                    "client_id": "CL004",
                    "carer": "Michael Johnson",
                    "phone": "01234 567 891",
                    "care_completed": True,
                    "reminders": "Speech exercises completed - pronunciation improving. Right arm strengthening exercises.",
                    "toilet": True,
                    "changed_clothes": True,
                    "food": "Soft diet breakfast, needs encouragement with swallowing. Thickened fluids as per speech therapy.",
                    "notes": "Dorothy completed all physiotherapy exercises today. Speech clarity improved. Excited about garden visit this afternoon - spotted new birds from window.",
                    "mood": ["determined", "optimistic", "excited about gardening"]
                },
                {
                    "client_id": "CL005",
                    "carer": "Lisa Chen",
                    "phone": "01234 567 892",
                    "care_completed": True,
                    "reminders": "Daily weight check: stable. Fluid restriction discussed. Heart medication administered.",
                    "toilet": True,
                    "changed_clothes": True,
                    "food": "Low-sodium breakfast. Monitored fluid intake carefully.",
                    "notes": "William's breathing comfortable today. No ankle swelling observed. Helped new resident settle in - natural mentor personality shining through.",
                    "mood": ["stable", "helpful", "mentor-like"]
                }
            ]

            for i, scenario in enumerate(visit_scenarios):
                for days_ago in range(min(3, len(visit_scenarios) - i)):
                    visit_logs.append(VisitLog(
                        id=f"VL{str(uuid.uuid4())[:8].upper()}",
                        client_id=scenario["client_id"],
                        carer_name=scenario["carer"],
                        carer_number=scenario["phone"],
                        date=datetime.now() - timedelta(days=days_ago, hours=random.randint(1, 8)),
                        personal_care_completed=scenario["care_completed"],
                        care_reminders_provided=scenario["reminders"],
                        toilet=scenario["toilet"],
                        changed_clothes=scenario["changed_clothes"],
                        ate_food=scenario["food"],
                        notes=scenario["notes"],
                        mood=scenario["mood"]
                    ))

            for visit_log in visit_logs:
                db.add(visit_log)

            print("Step 8: Creating audit logs")

            audit_actions = [
                ("admin@carehome.com", "login", "user", "admin@carehome.com"),
                ("manager@carehome.com", "created", "client", "CL001"),
                ("manager@carehome.com", "created", "schedule", "SCH001"),
                ("emily.watson@carehome.com", "login", "user", "emily.watson@carehome.com"),
                ("emily.watson@carehome.com", "created", "visit_log", "VL001"),
                ("emily.watson@carehome.com", "updated", "schedule_status", "SCH001"),
                ("manager@carehome.com", "assigned", "carer_client", "emily.watson@carehome.com-CL001"),
                ("admin@carehome.com", "created", "manager", "headmanager@carehome.com"),
                ("lisa.chen@carehome.com", "login", "user", "lisa.chen@carehome.com"),
                ("michael.johnson@carehome.com", "completed", "schedule", "SCH002"),
                ("family@demo.com", "viewed", "client", "CL001"),
                ("manager@carehome.com", "updated", "client", "CL002"),
            ]

            for i, (user_email, action, entity_type, entity_id) in enumerate(audit_actions):
                audit_log = AuditLog(
                    user_email=user_email,
                    action=action,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    timestamp=datetime.now() - timedelta(hours=random.randint(1, 72))
                )
                db.add(audit_log)

            db.commit()

            print("🎉 Database reset completed successfully!")
            print("\n" + "=" * 80)
            print("CAREVIEW DEMO DATABASE READY")
            print("=" * 80)
            print("\n DEMO ACCOUNTS: ")
            print("  Admin:    admin@demo.com / password123")
            print("  Manager:  manager@demo.com / password123")
            print("  Carer:    carer@demo.com / password123")
            print("  Family:   family@demo.com / password123")
            print("\nACCOUNTS:")
            print("  Manager:  manager@carehome.com / manager123")
            print("  Carer:    emily.watson@carehome.com / carer123")
            print("  Family:   john.smith@family.com / family123")
            print("\nDATA CREATED:")


            print("\n ACCESS POINTS:")
            print("  • API: http://localhost:8000")
            print("  • Docs: http://localhost:8000/docs")
            print("  • Health: http://localhost:8000/health")
            print("\n" + "=" * 80)

    except Exception as e:
        print(f" Database reset failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    reset_database()