from app.database import carers, managers, familys, patients
from app.models import UpdateCarer,VisitLog,LoginRequest,Token
from app.auth import hash_password,verify_password,create_access_token,get_current_carer,authenticate_carer
from fastapi import APIRouter, HTTPException, status, Depends





carer_router = APIRouter()




@carer_router.post("/carer/login", response_model=Token)
async def login_carer(login: LoginRequest):
    carer = authenticate_carer(login.email, login.password)     #Using our authenticate function to check if login valid
    if not carer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    #If successful login, create the token
    access_token = create_access_token(
        data={"sub": carer["email"]}  # 'sub' contains carer email
    )
    return {"access_token": access_token, "token_type": "bearer"}






#View own Details VIA TOKEN NOW!
@carer_router.get("/carer/me")
async def get_carer_details(current_carer: dict = Depends(get_current_carer)):
    return current_carer


#Change {email to /me





#View All Patients assigned to career
@carer_router.get("/carer/{email}/patients")
async def get_assigned_patients(email: str):
    # ✅ Check if the given email exists in the carers dictionary
    if email not in carers:
        return {"error": "Carer not found"}

    # ✅ Get the carer's profile
    carer = carers[email]

    # ✅ Get list of assigned patient IDs
    assigned_patient_ids = carer.get("assigned_patients", [])

    # ✅ Retrieve full patient data
    assigned_patient_data = [
        patients[pid] for pid in assigned_patient_ids if pid in patients
    ]

    # ✅ Return only the assigned patients' details
    return {"assigned_patients": assigned_patient_data}


#View specific patient ID which carer assigned to

@carer_router.get("/carer/{email}/patients/{id}")
async def get_assigned_patients_by_id(email: str, id: str):
    if email not in carers:
        return{"Error": "Carer not found"}

    carer = carers[email]
    assigned_patients_ids = carer.get("assigned_patients", [])
    if id not in assigned_patients_ids:
        return {"Error":"Patient not found"}

    patient = patients[id]
    return {"Patient":patient}




#Update Carer Details
@carer_router.put("/carer/{email}")
async def update_carer(email: str, new_data: UpdateCarer):
    if email not in carers:  # Check if carer exists
        return {"error": "Carer not found"}

    current = carers[email]  # Get current carer data
    update_data = new_data.dict(exclude_unset=True)  # Prepare update data
    new_email = update_data.get("email")  # Check if new email provided

    if new_email and new_email != email:  # If new email is different
        if new_email in carers:  # Check for email uniqueness
            return {"error": "This email is already in use!"}
        carers[new_email] = current  # Move data to new email key
        del carers[email]  # Delete old key
        email = new_email  # Update variable

    carers[email].update(update_data)  # Update fields
    return {"message": "Carer updated", "data": carers[email]}



#Create patient visit log

@carer_router.post("/carer/{email}/patients/{id}/visit-log")
async def create_visit_log(id: str, email: str,visitlog: VisitLog):
    visitlog = {

        "carer_email": carers[email]["email"],        #Not reentering valeus we already have
        "carer_number": carers[email]["phone"],
        "carer_name": carers[email]["name"],
        "patient_id": patients[id]["id"],
        "patient_name": patients[id]["name"],
        "date": visitlog.date,
        "showered": visitlog.showered,
        "meds_given": visitlog.meds_given,
        "toilet": visitlog.toilet,
        "changed_clothes": visitlog.changed_clothes,
        "ate_food": visitlog.ate_food,
        "notes": visitlog.notes,
        "mood": visitlog.mood or []
    }

    patient = patients[id]

    patient.visit_logs.append(visitlog)


    return {"message": "Visit log created successfully", "visit_log": visitlog}





