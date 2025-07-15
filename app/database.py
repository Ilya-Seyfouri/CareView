from datetime import datetime, date, time
from passlib.context import CryptContext
from uuid import uuid4

# Password hashing and verification
pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pass_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pass_context.verify(plain_password, hashed_password)


# System logs dictionaries
updates = {
    "Client Info Updated - C003 - 2024-07-14_09-00-00": {
        "Client Name": "William Thompson",
        "updated by": "Dr. Amanda Smith",
        "updated at": datetime(2024, 7, 14, 9, 0)
    },
    "Carer Details Updated - sarah.jones@healthcorp.com - 2024-07-14_10-30-00": {
        "Carer Name": "Sarah Jones",
        "updated by": "Jennifer Taylor",
        "updated at": datetime(2024, 7, 14, 10, 30)
    },
    "Visit Log Updated - VL005 - 2024-07-14_11-15-00": {
        "Client ID": "C004",
        "updated by": "Sarah Jones",
        "updated at": datetime(2024, 7, 14, 11, 15)
    }
}

# System logs with more recent carer activities
created = {
    "Client Created - C016 - 2024-07-14_08-30-00": {
        "Client name": "Patricia Wilson",
        "created by": "Dr. Amanda Smith",
        "created at": datetime(2024, 7, 14, 8, 30)
    },
    "Client Created - C017 - 2024-07-14_09-15-00": {
        "Client name": "Edward Martinez",
        "created by": "Jennifer Taylor",
        "created at": datetime(2024, 7, 14, 9, 15)
    },
    "Carer Created - jenny.davis@healthcorp.com - 2024-07-14_10-00-00": {
        "Carer name": "Jenny Davis",
        "created by": "Dr. Amanda Smith",
        "created at": datetime(2024, 7, 14, 10, 0)
    },
    "Visit Log Created - VL015 - 2024-07-14_11-30-00": {
        "Client ID": "C001",
        "created by": "Sarah Jones",
        "created at": datetime(2024, 7, 14, 11, 30)
    },
    "Visit Log Created - VL016 - 2024-07-14_12-45-00": {
        "Client ID": "C002",
        "created by": "Mike Wilson",
        "created at": datetime(2024, 7, 14, 12, 45)
    },
    "Schedule Created - SCH003 - 2024-07-14_13-00-00": {
        "created by": "Dr. Amanda Smith",
        "created at": datetime(2024, 7, 14, 13, 0)
    },
    "Family Member Created - robert.garcia@gmail.com - 2024-07-14_14-20-00": {
        "Family name": "Robert Garcia",
        "created by": "Jennifer Taylor",
        "created at": datetime(2024, 7, 14, 14, 20)
    },
    # Additional carer-related activities
    "Visit Log Created - VL017 - 2024-07-14_15-30-00": {
        "Client ID": "C004",
        "created by": "Sarah Jones",
        "created at": datetime(2024, 7, 14, 15, 30)
    },
    "Schedule Completed - SCH001 - 2024-07-14_10-45-00": {
        "Schedule ID": "SCH001",
        "completed by": "Sarah Jones",
        "created at": datetime(2024, 7, 14, 10, 45)
    },
    "Schedule Completed - SCH003 - 2024-07-14_11-15-00": {
        "Schedule ID": "SCH003",
        "completed by": "Emma Brown",
        "created at": datetime(2024, 7, 14, 11, 15)
    }
}

deleted = {}

# Admin accounts
admins = {
    "i.seyfouri@gmail.com": {
        "email": "i.seyfouri@gmail.com",
        "password": hash_password("loklok1354")
    }
}

# Enhanced schedules with multiple carers having visits today
schedules = {
    # Sarah Jones - 3 visits today (1 completed, 1 in progress, 1 scheduled)
    "SCH001": {
        "id": "SCH001",
        "carer_email": "sarah.jones@healthcorp.com",
        "client_id": "C004",
        "date": "2024-07-14",
        "start_time": "08:00",
        "end_time": "11:00",
        "shift_type": "morning",
        "status": "completed",
        "completed_at": "10:45",
        "notes": "Regular morning care routine",
        "created_by": "dr.smith@healthcorp.com",
        "created_at": datetime(2024, 7, 12, 10, 0)
    },
    "SCH009": {
        "id": "SCH009",
        "carer_email": "sarah.jones@healthcorp.com",
        "client_id": "C005",
        "date": "2024-07-14",
        "start_time": "12:00",
        "end_time": "15:00",
        "shift_type": "afternoon",
        "status": "in_progress",
        "notes": "Swallowing assistance and movement support",
        "created_by": "dr.smith@healthcorp.com",
        "created_at": datetime(2024, 7, 14, 8, 0)
    },
    "SCH010": {
        "id": "SCH010",
        "carer_email": "sarah.jones@healthcorp.com",
        "client_id": "C004",
        "date": "2026-07-14",
        "start_time": "16:00",
        "end_time": "19:00",
        "shift_type": "evening",
        "status": "scheduled",
        "notes": "Evening care and medication reminders",
        "created_by": "dr.smith@healthcorp.com",
        "created_at": datetime(2024, 7, 14, 9, 0)
    },

    # Mike Wilson - 2 visits today (1 completed, 1 scheduled)
    "SCH002": {
        "id": "SCH002",
        "carer_email": "mike.wilson@healthcorp.com",
        "client_id": "C001",
        "date": "2024-07-14",
        "start_time": "09:00",
        "end_time": "12:00",
        "shift_type": "morning",
        "status": "completed",
        "completed_at": "11:30",
        "notes": "Mobility support session completed",
        "created_by": "nurse.supervisor@healthcorp.com",
        "created_at": datetime(2024, 7, 12, 11, 30)
    },
    "SCH011": {
        "id": "SCH011",
        "carer_email": "mike.wilson@healthcorp.com",
        "client_id": "C006",
        "date": "2024-07-14",
        "start_time": "14:00",
        "end_time": "17:00",
        "shift_type": "afternoon",
        "status": "scheduled",
        "notes": "Recovery support and communication therapy",
        "created_by": "nurse.supervisor@healthcorp.com",
        "created_at": datetime(2024, 7, 14, 8, 30)
    },

    # Emma Brown - 2 visits today (both completed)
    "SCH003": {
        "id": "SCH003",
        "carer_email": "emma.brown@healthcorp.com",
        "client_id": "C010",
        "date": "2024-07-14",
        "start_time": "08:30",
        "end_time": "11:30",
        "shift_type": "morning",
        "status": "completed",
        "completed_at": "11:15",
        "notes": "Hip recovery support session",
        "created_by": "dr.smith@healthcorp.com",
        "created_at": datetime(2024, 7, 14, 8, 0)
    },
    "SCH012": {
        "id": "SCH012",
        "carer_email": "emma.brown@healthcorp.com",
        "client_id": "C010",
        "date": "2024-07-14",
        "start_time": "15:00",
        "end_time": "18:00",
        "shift_type": "afternoon",
        "status": "completed",
        "completed_at": "17:45",
        "notes": "Afternoon physiotherapy and personal care",
        "created_by": "dr.smith@healthcorp.com",
        "created_at": datetime(2024, 7, 14, 12, 0)
    },

    # Alex Taylor - 1 visit today (scheduled)
    "SCH004": {
        "id": "SCH004",
        "carer_email": "alex.taylor@healthcorp.com",
        "client_id": "C011",
        "date": "2024-07-14",
        "start_time": "10:30",
        "end_time": "13:30",
        "shift_type": "morning",
        "status": "scheduled",
        "notes": "Personal care and emotional support",
        "created_by": "care.coordinator@healthcorp.com",
        "created_at": datetime(2024, 7, 14, 7, 30)
    },

    # Lisa White - 1 visit today (scheduled)
    "SCH005": {
        "id": "SCH005",
        "carer_email": "lisa.white@healthcorp.com",
        "client_id": "C013",
        "date": "2024-07-14",
        "start_time": "20:00",
        "end_time": "23:00",
        "shift_type": "night",
        "status": "scheduled",
        "notes": "Night shift - memory support and wandering prevention",
        "created_by": "nurse.supervisor@healthcorp.com",
        "created_at": datetime(2024, 7, 14, 9, 0)
    },

    # David Green - 1 visit today (scheduled)
    "SCH006": {
        "id": "SCH006",
        "carer_email": "david.green@healthcorp.com",
        "client_id": "C015",
        "date": "2024-07-14",
        "start_time": "13:00",
        "end_time": "16:00",
        "shift_type": "afternoon",
        "status": "scheduled",
        "notes": "Prosthetic adaptation support",
        "created_by": "quality.assurance@healthcorp.com",
        "created_at": datetime(2024, 7, 14, 10, 15)
    },

    # Yesterday's completed schedules
    "SCH007": {
        "id": "SCH007",
        "carer_email": "sarah.jones@healthcorp.com",
        "client_id": "C005",
        "date": "2024-07-13",
        "start_time": "09:00",
        "end_time": "12:00",
        "shift_type": "morning",
        "status": "completed",
        "completed_at": "11:45",
        "notes": "Swallowing assistance and movement support",
        "created_by": "dr.smith@healthcorp.com",
        "created_at": datetime(2024, 7, 13, 8, 0)
    },
    "SCH008": {
        "id": "SCH008",
        "carer_email": "mike.wilson@healthcorp.com",
        "client_id": "C006",
        "date": "2024-07-13",
        "start_time": "11:00",
        "end_time": "15:00",
        "shift_type": "morning",
        "status": "completed",
        "completed_at": "14:30",
        "notes": "Recovery support and communication therapy",
        "created_by": "nurse.supervisor@healthcorp.com",
        "created_at": datetime(2024, 7, 13, 9, 30)
    },

    # Tomorrow's upcoming schedules
    "SCH013": {
        "id": "SCH013",
        "carer_email": "sarah.jones@healthcorp.com",
        "client_id": "C004",
        "date": "2024-07-15",
        "start_time": "08:00",
        "end_time": "11:00",
        "shift_type": "morning",
        "status": "scheduled",
        "notes": "Regular morning care routine",
        "created_by": "dr.smith@healthcorp.com",
        "created_at": datetime(2024, 7, 14, 15, 0)
    },
    "SCH014": {
        "id": "SCH014",
        "carer_email": "mike.wilson@healthcorp.com",
        "client_id": "C007",
        "date": "2024-07-15",
        "start_time": "10:00",
        "end_time": "13:00",
        "shift_type": "morning",
        "status": "scheduled",
        "notes": "Kidney support care routine",
        "created_by": "nurse.supervisor@healthcorp.com",
        "created_at": datetime(2024, 7, 14, 16, 0)
    }
}

# Enhanced carers with new staff member
carers = {
    "sarah.jones@healthcorp.com": {
        "email": "sarah.jones@healthcorp.com",
        "name": "Sarah Jones",
        "password": hash_password("sarah456"),
        "phone": "447987654321",
        "assigned_clients": ["C004", "C005"]
    },
    "mike.wilson@healthcorp.com": {
        "email": "mike.wilson@healthcorp.com",
        "name": "Mike Wilson",
        "password": hash_password("mike789"),
        "phone": "447555123456",
        "assigned_clients": ["C006", "C007", "C008", "C009"]
    },
    "emma.brown@healthcorp.com": {
        "email": "emma.brown@healthcorp.com",
        "name": "Emma Brown",
        "password": hash_password("emma321"),
        "phone": "447666789123",
        "assigned_clients": ["C010"]
    },
    "alex.taylor@healthcorp.com": {
        "email": "alex.taylor@healthcorp.com",
        "name": "Alex Taylor",
        "password": hash_password("alex999"),
        "phone": "447123987654",
        "assigned_clients": ["C011", "C012"]
    },
    "lisa.white@healthcorp.com": {
        "email": "lisa.white@healthcorp.com",
        "name": "Lisa White",
        "password": hash_password("lisa555"),
        "phone": "447888999000",
        "assigned_clients": ["C013", "C014"]
    },
    "david.green@healthcorp.com": {
        "email": "david.green@healthcorp.com",
        "name": "David Green",
        "password": hash_password("david777"),
        "phone": "447333444555",
        "assigned_clients": ["C015", "C001"]
    },
    "jenny.davis@healthcorp.com": {
        "email": "jenny.davis@healthcorp.com",
        "name": "Jenny Davis",
        "password": hash_password("jenny123"),
        "phone": "447999111222",
        "assigned_clients": ["C002", "C003"]
    }
}

# Enhanced family members with better contact distribution
familys = {
    "mary.johnson@gmail.com": {
        "id": "F001",
        "email": "mary.johnson@gmail.com",
        "name": "Mary Johnson",
        "password": hash_password("family123"),
        "phone": "447111222333",
        "assigned_clients": ["C001"]
    },
    "david.davis@outlook.com": {
        "id": "F002",
        "email": "david.davis@outlook.com",
        "name": "David Davis",
        "password": hash_password("family456"),
        "phone": "447444555666",
        "assigned_clients": ["C002"]
    },
    "linda.thompson@yahoo.com": {
        "id": "F003",
        "email": "linda.thompson@yahoo.com",
        "name": "Linda Thompson",
        "password": hash_password("family789"),
        "phone": "447777888999",
        "assigned_clients": ["C003"]
    },
    "susan.miller@gmail.com": {
        "id": "F004",
        "email": "susan.miller@gmail.com",
        "name": "Susan Miller",
        "password": hash_password("family321"),
        "phone": "447222333444",
        "assigned_clients": ["C004"]
    },
    "james.wilson@hotmail.com": {
        "id": "F005",
        "email": "james.wilson@hotmail.com",
        "name": "James Wilson Jr",
        "password": hash_password("family654"),
        "phone": "447555666777",
        "assigned_clients": ["C005"]
    },
    "carol.anderson@gmail.com": {
        "id": "F006",
        "email": "carol.anderson@gmail.com",
        "name": "Carol Anderson",
        "password": hash_password("family888"),
        "phone": "447999000111",
        "assigned_clients": ["C006"]
    },
    "robert.garcia@gmail.com": {
        "id": "F007",
        "email": "robert.garcia@gmail.com",
        "name": "Robert Garcia",
        "password": hash_password("family999"),
        "phone": "447333555777",
        "assigned_clients": ["C016"]
    },
    # Additional family members for better carer dashboard demo
    "patricia.miller@gmail.com": {
        "id": "F008",
        "email": "patricia.miller@gmail.com",
        "name": "Patricia Miller",
        "password": hash_password("family111"),
        "phone": "447111333555",
        "assigned_clients": ["C004"]  # Dorothy Miller's daughter
    },
    "charles.wilson.son@gmail.com": {
        "id": "F009",
        "email": "charles.wilson.son@gmail.com",
        "name": "Charles Wilson Jr",
        "password": hash_password("family222"),
        "phone": "447222444666",
        "assigned_clients": ["C005"]  # Charles Wilson's son
    },
    "rose.white.daughter@outlook.com": {
        "id": "F010",
        "email": "rose.white.daughter@outlook.com",
        "name": "Amanda White",
        "password": hash_password("family333"),
        "phone": "447333666999",
        "assigned_clients": ["C010"]  # Rose White's daughter
    },
    "arthur.smith.wife@gmail.com": {
        "id": "F011",
        "email": "arthur.smith.wife@gmail.com",
        "name": "Eleanor Smith",
        "password": hash_password("family444"),
        "phone": "447444777000",
        "assigned_clients": ["C011"]  # Arthur Smith's wife
    }
}

# Enhanced clients with recent visit logs and new clients
clients = {
    "C001": {
        "id": "C001",
        "name": "Robert Johnson",
        "age": 78,
        "room": "101A",
        "date_of_birth": "1946-03-15",
        "support_needs": "Personal care assistance, mobility support, medication reminders, requires assistance with daily activities and personal care routines.",
        "visit_logs": {
            "VL001": {
                "carer_name": "Dr. Amanda Smith",
                "id": "VL001",
                "date": "2024-07-10",
                "personal_care_completed": True,
                "care_reminders_provided": "Daily medication reminders provided as requested, all care preferences followed",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Enjoyed full breakfast, dietary preferences accommodated",
                "notes": "Client in good spirits today, enjoyed our chat about the garden. All care routines completed successfully.",
                "mood": ["happy", "cooperative"]
            },
            "VL002": {
                "carer_name": "Jennifer Taylor",
                "id": "VL002",
                "date": "2024-07-11",
                "personal_care_completed": False,
                "care_reminders_provided": "Evening care reminders provided as usual",
                "toilet": True,
                "changed_clothes": False,
                "ate_food": "Light dinner - appetite slightly reduced today",
                "notes": "Client mentioned feeling a bit tired. Provided extra comfort and support. Family contacted as requested.",
                "mood": ["tired", "concerned"]
            },
            "VL015": {
                "carer_name": "Sarah Jones",
                "id": "VL015",
                "date": "2024-07-14",
                "personal_care_completed": True,
                "care_reminders_provided": "Morning medication reminders given, mobility assistance provided",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Good appetite this morning, ate full breakfast",
                "notes": "Client much more energetic today. Completed morning exercises. Family visit scheduled for this afternoon.",
                "mood": ["cheerful", "energetic"]
            }
        }
    },
    "C002": {
        "id": "C002",
        "name": "Margaret Davis",
        "age": 82,
        "room": "102B",
        "date_of_birth": "1942-07-22",
        "support_needs": "Memory support, mobility assistance, fall prevention. Needs supervision and gentle encouragement for daily activities.",
        "visit_logs": {
            "VL003": {
                "carer_name": "Sarah Jones",
                "carer_number": "447987654321",
                "id": "VL003",
                "date": "2024-07-10",
                "personal_care_completed": True,
                "care_reminders_provided": "Daily care reminders provided with breakfast routine",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Breakfast well received - provided assistance as needed",
                "notes": "Client seemed a bit confused about the time but responded well to familiar carer. Peaceful night reported.",
                "mood": ["confused", "calm"]
            },
            "VL016": {
                "carer_name": "Mike Wilson",
                "id": "VL016",
                "date": "2024-07-14",
                "personal_care_completed": True,
                "care_reminders_provided": "Memory support provided, daily routine reinforced",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Assisted with lunch, ate well with encouragement",
                "notes": "Better orientation today. Client remembered carer's name and enjoyed conversation about her past.",
                "mood": ["alert", "nostalgic"]
            }
        }
    },
    "C003": {
        "id": "C003",
        "name": "William Thompson",
        "age": 75,
        "room": "103A",
        "date_of_birth": "1949-11-08",
        "support_needs": "Respiratory support, mobility assistance, emotional support. Requires breathing support equipment and limited mobility assistance.",
        "visit_logs": {
            "VL004": {
                "carer_name": "Mike Wilson",
                "carer_number": "447555123456",
                "id": "VL004",
                "date": "2024-07-11",
                "personal_care_completed": False,
                "care_reminders_provided": "Care reminders provided, breathing support equipment checked",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Small portions due to breathing comfort",
                "notes": "Breathing support working well today. Client positioned comfortably upright. Movement therapy session scheduled.",
                "mood": ["breathless", "determined"]
            }
        }
    },
    "C004": {
        "id": "C004",
        "name": "Dorothy Miller",
        "age": 88,
        "room": "201C",
        "date_of_birth": "1936-01-30",
        "support_needs": "Memory support, mobility assistance, personal care. Requires full assistance with personal care and gentle reassurance.",
        "visit_logs": {
            "VL005": {
                "carer_name": "Sarah Jones",
                "carer_number": "447987654321",
                "id": "VL005",
                "date": "2024-07-12",
                "personal_care_completed": True,
                "care_reminders_provided": "Daily care reminders provided, comfort support given for joint discomfort",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Soft diet well tolerated - appropriate texture provided",
                "notes": "Client seemed unsettled this morning. Used calming techniques and played familiar music. Mobility area checked - no concerns.",
                "mood": ["agitated", "calmer later"]
            },
            "VL006": {
                "carer_name": "Sarah Jones",
                "carer_number": "447987654321",
                "id": "VL006",
                "date": "2024-07-12",
                "personal_care_completed": False,
                "care_reminders_provided": "Afternoon comfort support provided",
                "toilet": True,
                "changed_clothes": False,
                "ate_food": "Lunch partially consumed with gentle assistance",
                "notes": "Client resting peacefully after lunch. Regular position changes provided for comfort.",
                "mood": ["peaceful", "sleepy"]
            }
        }
    },
    "C005": {
        "id": "C005",
        "name": "Charles Wilson",
        "age": 71,
        "room": "202A",
        "date_of_birth": "1953-09-12",
        "support_needs": "Movement support, swallowing assistance. Requires modified diet and movement support care.",
        "visit_logs": {
            "VL007": {
                "carer_name": "Sarah Jones",
                "carer_number": "447987654321",
                "id": "VL007",
                "date": "2024-07-11",
                "personal_care_completed": True,
                "care_reminders_provided": "Daily care reminders provided with modified diet assistance",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Thickened liquids and soft solids provided safely - no difficulties",
                "notes": "Movement challenges more noticeable today. Communication therapy session completed well. Swallow assessment scheduled for next week.",
                "mood": ["frustrated", "cooperative"]
            }
        }
    },
    "C006": {
        "id": "C006",
        "name": "Betty Anderson",
        "age": 79,
        "room": "203B",
        "date_of_birth": "1945-05-18",
        "support_needs": "Recovery support, left side weakness, communication assistance. Movement therapy ongoing.",
        "visit_logs": {
            "VL008": {
                "carer_name": "Mike Wilson",
                "carer_number": "447555123456",
                "id": "VL008",
                "date": "2024-07-10",
                "personal_care_completed": True,
                "care_reminders_provided": "Daily care reminders provided with thickened fluids",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Modified texture diet enjoyed well",
                "notes": "Movement therapy session went very well. Left arm movement showing slight improvement. Communication board used effectively.",
                "mood": ["determined", "proud"]
            }
        }
    },
    "C007": {
        "id": "C007",
        "name": "Frank Martinez",
        "age": 84,
        "room": "204A",
        "date_of_birth": "1940-12-03",
        "support_needs": "Kidney support care, dietary assistance, vision support. Special care routine 3x weekly.",
        "visit_logs": {
            "VL009": {
                "carer_name": "Mike Wilson",
                "carer_number": "447555123456",
                "id": "VL009",
                "date": "2024-07-09",
                "personal_care_completed": False,
                "care_reminders_provided": "Special care routine reminders provided - fluid monitoring followed",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Low-sodium, specialized breakfast - portion controlled as preferred",
                "notes": "Special care day. Client transported to care unit at 7:30 AM. Care access area checked - looking good.",
                "mood": ["tired", "resigned"]
            }
        }
    },
    "C008": {
        "id": "C008",
        "name": "Helen Garcia",
        "age": 76,
        "room": "205C",
        "date_of_birth": "1948-04-25",
        "support_needs": "Recovery support, anxiety management, comfort care. Comfort management care plan in place.",
        "visit_logs": {
            "VL010": {
                "carer_name": "Mike Wilson",
                "carer_number": "447555123456",
                "id": "VL010",
                "date": "2024-07-11",
                "personal_care_completed": True,
                "care_reminders_provided": "Comfort care reminders provided, anxiety support given - comfort level improved from 6/10 to 3/10",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Small appetite due to comfort care effects",
                "notes": "Comfort management effective today. Client attended art therapy session. Support specialist follow-up scheduled for next week.",
                "mood": ["anxious", "relieved"]
            }
        }
    },
    "C009": {
        "id": "C009",
        "name": "George Lee",
        "age": 80,
        "room": "206B",
        "date_of_birth": "1944-08-14",
        "support_needs": "Mobility support, wheelchair assistance, bladder care support. Requires specialized mobility care.",
        "visit_logs": {
            "VL011": {
                "carer_name": "Mike Wilson",
                "carer_number": "447555123456",
                "id": "VL011",
                "date": "2024-07-12",
                "personal_care_completed": True,
                "care_reminders_provided": "Mobility care reminders provided, muscle support care management",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Regular diet - good appetite maintained",
                "notes": "Specialized care completed. Pressure relief cushion adjusted. Independence therapy assessment completed.",
                "mood": ["optimistic", "chatty"]
            }
        }
    },
    "C010": {
        "id": "C010",
        "name": "Rose White",
        "age": 73,
        "room": "301A",
        "date_of_birth": "1951-10-07",
        "support_needs": "Recovery support after hip procedure, mobility assistance, mild cognitive support. Rehabilitation in progress.",
        "visit_logs": {
            "VL012": {
                "carer_name": "Emma Brown",
                "carer_number": "447666789123",
                "id": "VL012",
                "date": "2024-07-10",
                "personal_care_completed": False,
                "care_reminders_provided": "Recovery care reminders provided, bone health support - post-procedure care routine",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "High-protein diet for healing - ate well",
                "notes": "Hip recovery progressing well. Movement therapy session focused on mobility. Weight-bearing as comfortable.",
                "mood": ["motivated", "hopeful"]
            }
        }
    },
    "C011": {
        "id": "C011",
        "name": "Arthur Smith",
        "age": 77,
        "room": "302B",
        "date_of_birth": "1947-06-20",
        "support_needs": "Personal care support, continence assistance, emotional support. Regular specialist follow-ups required.",
        "visit_logs": {}
    },
    "C012": {
        "id": "C012",
        "name": "Joyce Green",
        "age": 85,
        "room": "303A",
        "date_of_birth": "1939-02-14",
        "support_needs": "Vision support, hearing assistance, mobility support. Requires sensory support aids.",
        "visit_logs": {}
    },
    "C013": {
        "id": "C013",
        "name": "Harold Brown",
        "age": 81,
        "room": "304B",
        "date_of_birth": "1943-08-05",
        "support_needs": "Memory support, wandering prevention, sleep support. Requires constant supervision and gentle guidance.",
        "visit_logs": {
            "VL013": {
                "carer_name": "Lisa White",
                "carer_number": "447888999000",
                "id": "VL013",
                "date": "2024-07-12",
                "personal_care_completed": False,
                "care_reminders_provided": "Evening care reminders provided, natural sleep support given",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Light evening snack",
                "notes": "Night shift - client attempted to leave room twice. Redirected using gentle guidance and validation. Settled after warm drink.",
                "mood": ["restless", "confused"]
            }
        }
    },
    "C014": {
        "id": "C014",
        "name": "Ethel King",
        "age": 76,
        "room": "305A",
        "date_of_birth": "1948-12-18",
        "support_needs": "Kidney support care, circulatory support, energy support. Requires fluid monitoring and specialized care.",
        "visit_logs": {}
    },
    "C015": {
        "id": "C015",
        "name": "Raymond Clark",
        "age": 74,
        "room": "306C",
        "date_of_birth": "1950-04-02",
        "support_needs": "Adaptation support, phantom sensation management, emotional support. Prosthetic fitting in progress.",
        "visit_logs": {
            "VL014": {
                "carer_name": "David Green",
                "carer_number": "447333444555",
                "id": "VL014",
                "date": "2024-07-11",
                "personal_care_completed": True,
                "care_reminders_provided": "Adaptation support care provided for phantom sensations, emotional support care given",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Regular diet - appetite improving",
                "notes": "Prosthetic fitting appointment went well. Sensation management working effectively. Client showing more interest in activities.",
                "mood": ["encouraged", "hopeful"]
            }
        }
    },
    "C016": {
        "id": "C016",
        "name": "Patricia Wilson",
        "age": 69,
        "room": "307A",
        "date_of_birth": "1955-03-22",
        "support_needs": "Post-surgery recovery, wound care, mobility support. Requires assistance with daily activities during recovery period.",
        "visit_logs": {}
    },
    "C017": {
        "id": "C017",
        "name": "Edward Martinez",
        "age": 83,
        "room": "308B",
        "date_of_birth": "1941-09-14",
        "support_needs": "Advanced memory support, 24-hour supervision, behavioral support. Requires specialized memory care approach.",
        "visit_logs": {}
    }
}

# Manager accounts
managers = {
    "dr.smith@healthcorp.com": {
        "email": "dr.smith@healthcorp.com",
        "name": "Dr. Amanda Smith",
        "password": hash_password("manager123"),
        "department": "Medical Director"
    },
    "nurse.supervisor@healthcorp.com": {
        "email": "nurse.supervisor@healthcorp.com",
        "name": "Jennifer Taylor",
        "password": hash_password("manager456"),
        "department": "Nursing Supervisor"
    },
    "admin.head@healthcorp.com": {
        "email": "admin.head@healthcorp.com",
        "name": "Robert Chen",
        "password": hash_password("manager789"),
        "department": "Administration"
    },
    "care.coordinator@healthcorp.com": {
        "email": "care.coordinator@healthcorp.com",
        "name": "Lisa Rodriguez",
        "password": hash_password("manager321"),
        "department": "Care Coordination"
    },
    "quality.assurance@healthcorp.com": {
        "email": "quality.assurance@healthcorp.com",
        "name": "Michael Thompson",
        "password": hash_password("manager555"),
        "department": "Quality Assurance"
    }
}