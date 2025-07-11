from datetime import date
from passlib.context import CryptContext
pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# creating cryptcontext object which handles password hashing settings


def hash_password(password: str) -> str:  # returns hashed password using bcrypt
    return pass_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pass_context.verify(plain_password, hashed_password)

carers = {
    "sarah.jones@healthcorp.com": {
        "email": "sarah.jones@healthcorp.com",
        "name": "Sarah Jones",
        "password": hash_password("sarah456"),  # Plain password: sarah456
        "phone": 447987654321.0,
        "assigned_patients": ["P004", "P005"]
    },
    "mike.wilson@healthcorp.com": {
        "email": "mike.wilson@healthcorp.com",
        "name": "Mike Wilson",
        "password": hash_password("mike789"),  # Plain password: mike789
        "phone": 447555123456.0,
        "assigned_patients": ["P006", "P007", "P008", "P009"]
    },
    "emma.brown@healthcorp.com": {
        "email": "emma.brown@healthcorp.com",
        "name": "Emma Brown",
        "password": hash_password("emma321"),  # Plain password: emma321
        "phone": 447666789123.0,
        "assigned_patients": ["P010"]
    },
    "alex.taylor@healthcorp.com": {
        "email": "alex.taylor@healthcorp.com",
        "name": "Alex Taylor",
        "password": hash_password("alex999"),  # Plain password: alex999
        "phone": 447123987654.0,
        "assigned_patients": ["P011", "P012"]
    },
    "lisa.white@healthcorp.com": {
        "email": "lisa.white@healthcorp.com",
        "name": "Lisa White",
        "password": hash_password("lisa555"),  # Plain password: lisa555
        "phone": 447888999000.0,
        "assigned_patients": ["P013", "P014"]
    },
    "david.green@healthcorp.com": {
        "email": "david.green@healthcorp.com",
        "name": "David Green",
        "password": hash_password("david777"),  # Plain password: david777
        "phone": 447333444555.0,
        "assigned_patients": ["P015"]
    }
}

familys = {
    "mary.johnson@gmail.com": {
        "id": "F001",
        "email": "mary.johnson@gmail.com",
        "name": "Mary Johnson",
        "password": hash_password("family123"),  # Plain password: family123
        "phone": 447111222333.0,
        "assigned_patients": ["P001"]
    },
    "david.davis@outlook.com": {
        "id": "F002",
        "email": "david.davis@outlook.com",
        "name": "David Davis",
        "password": hash_password("family456"),  # Plain password: family456
        "phone": 447444555666.0,
        "assigned_patients": ["P002"]
    },
    "linda.thompson@yahoo.com": {
        "id": "F003",
        "email": "linda.thompson@yahoo.com",
        "name": "Linda Thompson",
        "password": hash_password("family789"),  # Plain password: family789
        "phone": 447777888999.0,
        "assigned_patients": ["P003"]
    },
    "susan.miller@gmail.com": {
        "id": "F004",
        "email": "susan.miller@gmail.com",
        "name": "Susan Miller",
        "password": hash_password("family321"),  # Plain password: family321
        "phone": 447222333444.0,
        "assigned_patients": ["P004"]
    },
    "james.wilson@hotmail.com": {
        "id": "F005",
        "email": "james.wilson@hotmail.com",
        "name": "James Wilson Jr",
        "password": hash_password("family654"),  # Plain password: family654
        "phone": 447555666777.0,
        "assigned_patients": ["P005"]
    },
    "carol.anderson@gmail.com": {
        "id": "F006",
        "email": "carol.anderson@gmail.com",
        "name": "Carol Anderson",
        "password": hash_password("family888"),  # Plain password: family888
        "phone": 447999000111.0,
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
        "visit_logs": {}
    },
    "P002": {
        "id": "P002",
        "name": "Margaret Davis",
        "age": 82,
        "room": "102B",
        "date_of_birth": date(1942, 7, 22),
        "medical_history": "Alzheimer's disease, Osteoporosis, Falls risk. Needs supervision for all daily activities.",
        "visit_logs": {}
    },
    "P003": {
        "id": "P003",
        "name": "William Thompson",
        "age": 75,
        "room": "103A",
        "date_of_birth": date(1949, 11, 8),
        "medical_history": "COPD, Heart failure, Depression. Oxygen therapy required, limited mobility.",
        "visit_logs": {}
    },
    "P004": {
        "id": "P004",
        "name": "Dorothy Miller",
        "age": 88,
        "room": "201C",
        "date_of_birth": date(1936, 1, 30),
        "medical_history": "Dementia, Arthritis, Previous hip fracture. Requires full assistance with personal care.",
        "visit_logs": {}
    },
    "P005": {
        "id": "P005",
        "name": "Charles Wilson",
        "age": 71,
        "room": "202A",
        "date_of_birth": date(1953, 9, 12),
        "medical_history": "Parkinson's disease, Swallowing difficulties. Requires modified diet and medication support.",
        "visit_logs": {}
    },
    "P006": {
        "id": "P006",
        "name": "Betty Anderson",
        "age": 79,
        "room": "203B",
        "date_of_birth": date(1945, 5, 18),
        "medical_history": "Stroke survivor, Left side weakness, Speech difficulties. Physiotherapy ongoing.",
        "visit_logs": {}
    },
    "P007": {
        "id": "P007",
        "name": "Frank Martinez",
        "age": 84,
        "room": "204A",
        "date_of_birth": date(1940, 12, 3),
        "medical_history": "Kidney disease, Diabetes, Vision impairment. Dialysis 3x weekly.",
        "visit_logs": {}
    },
    "P008": {
        "id": "P008",
        "name": "Helen Garcia",
        "age": 76,
        "room": "205C",
        "date_of_birth": date(1948, 4, 25),
        "medical_history": "Breast cancer survivor, Anxiety, Chronic pain. Pain management protocol in place.",
        "visit_logs": {}
    },
    "P009": {
        "id": "P009",
        "name": "George Lee",
        "age": 80,
        "room": "206B",
        "date_of_birth": date(1944, 8, 14),
        "medical_history": "Multiple sclerosis, Wheelchair bound, Bladder incontinence. Requires specialized care.",
        "visit_logs": {}
    },
    "P010": {
        "id": "P010",
        "name": "Rose White",
        "age": 73,
        "room": "301A",
        "date_of_birth": date(1951, 10, 7),
        "medical_history": "Recent hip replacement, Osteoarthritis, Mild cognitive decline. Rehabilitation in progress.",
        "visit_logs": {}
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
        "visit_logs": {}
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
        "visit_logs": {}
    }
}

managers = {
    "dr.smith@healthcorp.com": {
        "email": "dr.smith@healthcorp.com",
        "name": "Dr. Amanda Smith",
        "password": hash_password("manager123"),  # Plain password: manager123
        "department": "Medical Director"
    },
    "nurse.supervisor@healthcorp.com": {
        "email": "nurse.supervisor@healthcorp.com",
        "name": "Jennifer Taylor",
        "password": hash_password("manager456"),  # Plain password: manager456
        "department": "Nursing Supervisor"
    },
    "admin.head@healthcorp.com": {
        "email": "admin.head@healthcorp.com",
        "name": "Robert Chen",
        "password": hash_password("manager789"),  # Plain password: manager789
        "department": "Administration"
    },
    "care.coordinator@healthcorp.com": {
        "email": "care.coordinator@healthcorp.com",
        "name": "Lisa Rodriguez",
        "password": hash_password("manager321"),  # Plain password: manager321
        "department": "Care Coordination"
    },
    "quality.assurance@healthcorp.com": {
        "email": "quality.assurance@healthcorp.com",
        "name": "Michael Thompson",
        "password": hash_password("manager555"),  # Plain password: manager555
        "department": "Quality Assurance"
    }
}
