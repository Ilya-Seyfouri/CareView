from datetime import datetime, date,time
from passlib.context import CryptContext
pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from uuid import uuid4

# Password hashing and verification
def hash_password(password: str) -> str:
    return pass_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pass_context.verify(plain_password, hashed_password)


schedules = {
    "SCH001": {
        "id": "SCH001",
        "carer_email": "sarah.jones@healthcorp.com",
        "patient_id": "P004",
        "date": date(2024, 7, 15),
        "start_time": time(8, 0),
        "end_time": time(16, 0),
        "shift_type": "morning",
        "status": "scheduled",
        "notes": "Regular morning care routine",
        "created_by": "dr.smith@healthcorp.com",
        "created_at": datetime(2024, 7, 12, 10, 0)
    },
    "SCH002": {
        "id": "SCH002",
        "carer_email": "mike.wilson@healthcorp.com",
        "patient_id": "P001",
        "date": date(2024, 7, 15),
        "start_time": time(14, 0),
        "end_time": time(18, 0),
        "shift_type": "afternoon",
        "status": "scheduled",
        "notes": "Physiotherapy session included",
        "created_by": "nurse.supervisor@healthcorp.com",
        "created_at": datetime(2024, 7, 12, 11, 30)
    }
}

carers = {
    "sarah.jones@healthcorp.com": {
        "email": "sarah.jones@healthcorp.com",
        "name": "Sarah Jones",
        "password": hash_password("sarah456"),
        "phone": "447987654321",
        "assigned_patients": ["P004", "P005"]
    },
    "mike.wilson@healthcorp.com": {
        "email": "mike.wilson@healthcorp.com",
        "name": "Mike Wilson",
        "password": hash_password("mike789"),
        "phone": "447555123456",
        "assigned_patients": ["P006", "P007", "P008", "P009"]
    },
    "emma.brown@healthcorp.com": {
        "email": "emma.brown@healthcorp.com",
        "name": "Emma Brown",
        "password": hash_password("emma321"),
        "phone": "447666789123",
        "assigned_patients": ["P010"]
    },
    "alex.taylor@healthcorp.com": {
        "email": "alex.taylor@healthcorp.com",
        "name": "Alex Taylor",
        "password": hash_password("alex999"),
        "phone": "447123987654",
        "assigned_patients": ["P011", "P012"]
    },
    "lisa.white@healthcorp.com": {
        "email": "lisa.white@healthcorp.com",
        "name": "Lisa White",
        "password": hash_password("lisa555"),
        "phone": "447888999000",
        "assigned_patients": ["P013", "P014"]
    },
    "david.green@healthcorp.com": {
        "email": "david.green@healthcorp.com",
        "name": "David Green",
        "password": hash_password("david777"),
        "phone": "447333444555",
        "assigned_patients": ["P015"]
    }
}

familys = {
    "mary.johnson@gmail.com": {
        "id": "F001",
        "email": "mary.johnson@gmail.com",
        "name": "Mary Johnson",
        "password": hash_password("family123"),
        "phone": "447111222333",
        "assigned_patients": ["P001"]
    },
    "david.davis@outlook.com": {
        "id": "F002",
        "email": "david.davis@outlook.com",
        "name": "David Davis",
        "password": hash_password("family456"),
        "phone": "447444555666",
        "assigned_patients": ["P002"]
    },
    "linda.thompson@yahoo.com": {
        "id": "F003",
        "email": "linda.thompson@yahoo.com",
        "name": "Linda Thompson",
        "password": hash_password("family789"),
        "phone": "447777888999",
        "assigned_patients": ["P003"]
    },
    "susan.miller@gmail.com": {
        "id": "F004",
        "email": "susan.miller@gmail.com",
        "name": "Susan Miller",
        "password": hash_password("family321"),
        "phone": "447222333444",
        "assigned_patients": ["P004"]
    },
    "james.wilson@hotmail.com": {
        "id": "F005",
        "email": "james.wilson@hotmail.com",
        "name": "James Wilson Jr",
        "password": hash_password("family654"),
        "phone": "447555666777",
        "assigned_patients": ["P005"]
    },
    "carol.anderson@gmail.com": {
        "id": "F006",
        "email": "carol.anderson@gmail.com",
        "name": "Carol Anderson",
        "password": hash_password("family888"),
        "phone": "447999000111",
        "assigned_patients": ["P006"]
    }
}

patients = {
    "P001": {
        "id": "P001",
        "name": "Robert Johnson",
        "age": 78,
        "room": "101A",
        "date_of_birth": date(1946, 3, 15),
        "medical_history": "Diabetes Type 2, Hypertension, Previous stroke in 2020. Requires assistance with mobility and medication management.",
        "visit_logs": {
            "VL001": {
                "carer_name": "Dr. Amanda Smith",
                "id": "VL001",
                "date": datetime(2024, 7, 10, 8, 30),
                "showered": True,
                "meds_given": "Metformin 500mg, Lisinopril 10mg - All medications administered as prescribed",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Full breakfast consumed - diabetic meal plan followed",
                "notes": "Patient in good spirits today. Blood sugar levels stable. Assisted with morning routine.",
                "mood": ["happy", "cooperative"]
            },
            "VL002": {
                "carer_name": "Jennifer Taylor",
                "id": "VL002",
                "date": datetime(2024, 7, 11, 9, 15),
                "showered": False,
                "meds_given": "Evening medications - Metformin 500mg administered",
                "toilet": True,
                "changed_clothes": False,
                "ate_food": "Light dinner - appetite slightly reduced",
                "notes": "Patient complained of mild dizziness. Vitals checked and documented. Family notified.",
                "mood": ["tired", "concerned"]
            }
        }
    },
    "P002": {
        "id": "P002",
        "name": "Margaret Davis",
        "age": 82,
        "room": "102B",
        "date_of_birth": date(1942, 7, 22),
        "medical_history": "Alzheimer's disease, Osteoporosis, Falls risk. Needs supervision for all daily activities.",
        "visit_logs": {
            "VL003": {
                "carer_name": "Sarah Jones",
                "carer_number": "447987654321",
                "id": "VL003",
                "date": datetime(2024, 7, 10, 7, 45),
                "showered": True,
                "meds_given": "Donepezil 10mg, Calcium supplements - All medications given with breakfast",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Breakfast well received - assisted feeding required",
                "notes": "Patient was confused about location but responded well to familiar carer. No incidents overnight.",
                "mood": ["confused", "calm"]
            }
        }
    },
    "P003": {
        "id": "P003",
        "name": "William Thompson",
        "age": 75,
        "room": "103A",
        "date_of_birth": date(1949, 11, 8),
        "medical_history": "COPD, Heart failure, Depression. Oxygen therapy required, limited mobility.",
        "visit_logs": {
            "VL004": {
                "carer_name": "Mike Wilson",
                "carer_number": "447555123456",
                "id": "VL004",
                "date": datetime(2024, 7, 11, 10, 30),
                "showered": False,
                "meds_given": "Furosemide 40mg, Sertraline 50mg, Bronchodilator inhaler used",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Small portions due to shortness of breath",
                "notes": "Oxygen saturation 92%. Chest slightly tight today. Positioned upright for comfort. Physiotherapy session scheduled.",
                "mood": ["breathless", "determined"]
            }
        }
    },
    "P004": {
        "id": "P004",
        "name": "Dorothy Miller",
        "age": 88,
        "room": "201C",
        "date_of_birth": date(1936, 1, 30),
        "medical_history": "Dementia, Arthritis, Previous hip fracture. Requires full assistance with personal care.",
        "visit_logs": {
            "VL005": {
                "carer_name": "Sarah Jones",
                "carer_number": "447987654321",
                "id": "VL005",
                "date": datetime(2024, 7, 12, 8, 0),
                "showered": True,
                "meds_given": "Memantine 10mg, Paracetamol for joint pain - all administered",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Soft diet well tolerated - pureed consistency",
                "notes": "Patient very agitated this morning. Used calming techniques and familiar music. Hip area checked - no concerns.",
                "mood": ["agitated", "calmer later"]
            },
            "VL006": {
                "carer_name": "Sarah Jones",
                "carer_number": "447987654321",
                "id": "VL006",
                "date": datetime(2024, 7, 12, 14, 30),
                "showered": False,
                "meds_given": "Afternoon pain relief administered",
                "toilet": True,
                "changed_clothes": False,
                "ate_food": "Lunch partially consumed with assistance",
                "notes": "Patient sleeping peacefully after lunch. Turned every 2 hours to prevent pressure sores.",
                "mood": ["peaceful", "sleepy"]
            }
        }
    },
    "P005": {
        "id": "P005",
        "name": "Charles Wilson",
        "age": 71,
        "room": "202A",
        "date_of_birth": date(1953, 9, 12),
        "medical_history": "Parkinson's disease, Swallowing difficulties. Requires modified diet and medication support.",
        "visit_logs": {
            "VL007": {
                "carer_name": "Sarah Jones",
                "carer_number": "447987654321",
                "id": "VL007",
                "date": datetime(2024, 7, 11, 9, 0),
                "showered": True,
                "meds_given": "Levodopa 100mg, Ropinirole 2mg - crushed and mixed with applesauce",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Thickened liquids and soft solids - no choking incidents",
                "notes": "Tremor more pronounced today. Speech therapy session completed. Swallow assessment due next week.",
                "mood": ["frustrated", "cooperative"]
            }
        }
    },
    "P006": {
        "id": "P006",
        "name": "Betty Anderson",
        "age": 79,
        "room": "203B",
        "date_of_birth": date(1945, 5, 18),
        "medical_history": "Stroke survivor, Left side weakness, Speech difficulties. Physiotherapy ongoing.",
        "visit_logs": {
            "VL008": {
                "carer_name": "Mike Wilson",
                "carer_number": "447555123456",
                "id": "VL008",
                "date": datetime(2024, 7, 10, 11, 15),
                "showered": True,
                "meds_given": "Aspirin 75mg, Atorvastatin 20mg - medications given with thickened water",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Modified texture diet consumed well",
                "notes": "Physiotherapy session went well. Left arm movement improving slightly. Communication board used effectively.",
                "mood": ["determined", "proud"]
            }
        }
    },
    "P007": {
        "id": "P007",
        "name": "Frank Martinez",
        "age": 84,
        "room": "204A",
        "date_of_birth": date(1940, 12, 3),
        "medical_history": "Kidney disease, Diabetes, Vision impairment. Dialysis 3x weekly.",
        "visit_logs": {
            "VL009": {
                "carer_name": "Mike Wilson",
                "carer_number": "447555123456",
                "id": "VL009",
                "date": datetime(2024, 7, 9, 6, 30),
                "showered": False,
                "meds_given": "Pre-dialysis medications administered - fluid restricted",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Low-sodium, diabetic breakfast - portion controlled",
                "notes": "Dialysis day. Patient transported to unit at 7:30 AM. Access site checked - no signs of infection.",
                "mood": ["tired", "resigned"]
            }
        }
    },
    "P008": {
        "id": "P008",
        "name": "Helen Garcia",
        "age": 76,
        "room": "205C",
        "date_of_birth": date(1948, 4, 25),
        "medical_history": "Breast cancer survivor, Anxiety, Chronic pain. Pain management protocol in place.",
        "visit_logs": {
            "VL010": {
                "carer_name": "Mike Wilson",
                "carer_number": "447555123456",
                "id": "VL010",
                "date": datetime(2024, 7, 11, 13, 45),
                "showered": True,
                "meds_given": "Morphine 5mg, Lorazepam 0.5mg for anxiety - pain level 6/10 before, 3/10 after",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Small appetite due to medication effects",
                "notes": "Pain management effective today. Patient attended art therapy session. Oncology follow-up scheduled for next week.",
                "mood": ["anxious", "relieved"]
            }
        }
    },
    "P009": {
        "id": "P009",
        "name": "George Lee",
        "age": 80,
        "room": "206B",
        "date_of_birth": date(1944, 8, 14),
        "medical_history": "Multiple sclerosis, Wheelchair bound, Bladder incontinence. Requires specialized care.",
        "visit_logs": {
            "VL011": {
                "carer_name": "Mike Wilson",
                "carer_number": "447555123456",
                "id": "VL011",
                "date": datetime(2024, 7, 12, 10, 0),
                "showered": True,
                "meds_given": "Baclofen 10mg, Vitamin D supplement - muscle spasticity management",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Regular diet - good appetite maintained",
                "notes": "Catheter care completed. Pressure relief cushion adjusted. Occupational therapy assessment completed.",
                "mood": ["optimistic", "chatty"]
            }
        }
    },
    "P010": {
        "id": "P010",
        "name": "Rose White",
        "age": 73,
        "room": "301A",
        "date_of_birth": date(1951, 10, 7),
        "medical_history": "Recent hip replacement, Osteoarthritis, Mild cognitive decline. Rehabilitation in progress.",
        "visit_logs": {
            "VL012": {
                "carer_name": "Emma Brown",
                "carer_number": "447666789123",
                "id": "VL012",
                "date": datetime(2024, 7, 10, 9, 30),
                "showered": False,
                "meds_given": "Tramadol 50mg, Calcium with Vitamin D - post-surgical care protocol",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "High-protein diet for healing - ate well",
                "notes": "Hip replacement healing well. Physiotherapy session focused on mobility. Weight-bearing as tolerated.",
                "mood": ["motivated", "hopeful"]
            }
        }
    },
    "P011": {
        "id": "P011",
        "name": "Arthur Smith",
        "age": 77,
        "room": "302B",
        "date_of_birth": date(1947, 6, 20),
        "medical_history": "Prostate cancer, Incontinence, Mild depression. Regular oncology follow-ups required.",
        "visit_logs": {}
    },
    "P012": {
        "id": "P012",
        "name": "Joyce Green",
        "age": 85,
        "room": "303A",
        "date_of_birth": date(1939, 2, 14),
        "medical_history": "Macular degeneration, Hearing loss, Mobility issues. Requires sensory support aids.",
        "visit_logs": {}
    },
    "P013": {
        "id": "P013",
        "name": "Harold Brown",
        "age": 81,
        "room": "304B",
        "date_of_birth": date(1943, 8, 5),
        "medical_history": "Alzheimer's disease, Wandering behavior, Sleep disturbances. Requires constant supervision.",
        "visit_logs": {
            "VL013": {
                "carer_name": "Lisa White",
                "carer_number": "447888999000",
                "id": "VL013",
                "date": datetime(2024, 7, 12, 22, 30),
                "showered": False,
                "meds_given": "Evening Donepezil 10mg, Melatonin 3mg for sleep",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Light evening snack",
                "notes": "Night shift - patient attempted to leave room twice. Redirected using validation therapy. Settled after warm milk.",
                "mood": ["restless", "confused"]
            }
        }
    },
    "P014": {
        "id": "P014",
        "name": "Ethel King",
        "age": 76,
        "room": "305A",
        "date_of_birth": date(1948, 12, 18),
        "medical_history": "Chronic kidney disease, Hypertension, Anemia. Requires fluid monitoring and dialysis.",
        "visit_logs": {}
    },
    "P015": {
        "id": "P015",
        "name": "Raymond Clark",
        "age": 74,
        "room": "306C",
        "date_of_birth": date(1950, 4, 2),
        "medical_history": "Recent amputation, Phantom limb pain, Depression. Prosthetic fitting in progress.",
        "visit_logs": {
            "VL014": {
                "carer_name": "David Green",
                "carer_number": "447333444555",
                "id": "VL014",
                "date": datetime(2024, 7, 11, 16, 0),
                "showered": True,
                "meds_given": "Gabapentin 300mg for phantom pain, Sertraline 100mg for depression",
                "toilet": True,
                "changed_clothes": True,
                "ate_food": "Regular diet - appetite improving",
                "notes": "Prosthetic fitting appointment went well. Phantom pain managed effectively. Patient showing more interest in activities.",
                "mood": ["encouraged", "hopeful"]
            }
        }
    }
}

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