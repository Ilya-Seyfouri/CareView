# CareView - Care Home Management System

A comprehensive care home management system designed for professional healthcare facilities with digital care
tracking and staff coordination. The system utilizes a PostgreSQL database for secure healthcare data storage,
FastAPI backend for robust REST API services, and role-based authentication to ensure compliant access control.


# Visit the Site
<link>



## Quick Start - Demo Accounts

Try it out with these accounts (or just click demo mode on the site):
- **Manager**: `manager@demo.com` / `password123`
- **Carer**: `carer@demo.com` / `password123`  
- **Family**: `family@demo.com` / `password123`

## What it does

- Track resident care visits and notes
- Schedule staff shifts (prevents double-booking) 
- Let families see care updates
- Manager dashboard with oversight
- Full audit trail for compliance
# CareView - Care Home Management System

Built for real care home workflows - not just a prototype.

## Tech Stack

- **Backend**: FastAPI + PostgreSQL 
- **Auth**: JWT tokens, bcrypt passwords
- **Access control**: Role-based (manager/carer/family)
- **Documentation**: Auto-generated at `/docs`

## Setup

Need Python 3.8+, PostgreSQL, and Git.

```bash
git clone https://github.com/yourusername/careview-system.git
cd careview-system

# Virtual environment
python -m venv careview-env
source careview-env/bin/activate  # Windows: careview-env\Scripts\activate

# Install stuff
pip install -r requirements.txt

# Database config - create .env file:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=careview
DB_USER=your_username
DB_PASSWORD=your_password
SECRET_KEY=your_jwt_secret_key

# Set up database with sample data
python scripts/reset.py

# Run it
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Using it

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- System status: `http://localhost:8000/status`

### Main endpoints

**Auth stuff:**
- `POST /login` - Log in, get JWT token
- `GET /me` - Your profile info

**Manager functions:**
- `GET /manager/clients` - Manage residents
- `GET /manager/carers` - Staff accounts
- `GET /manager/schedules` - Shift planning
- `GET /manager/dashboard` - Overview

**Carer functions:**
- `GET /carer/me/clients` - Your assigned residents
- `GET /carer/me/schedules` - Your shifts
- `POST /carer/me/clients/{id}/visit-log` - Log a visit

**Family access:**
- `GET /family/me/clients` - Family member's care info
- `GET /family/me/schedules` - Upcoming visits
- `GET /family/me/today` - Today's summary

## Testing

```bash
pytest tests/ -v
```

Tests cover auth, permissions, CRUD operations, and error handling.

## How it's built

### Database design
- Single user table with roles (simpler than separate tables)
- Many-to-many carer/client assignments  
- Audit logging for everything
- Schedule conflict prevention

### Security
- JWT auth (8 hour expiry)
- bcrypt password hashing
- Input validation
- Role-based access control
- Activity logging

### API structure
- FastAPI with auto docs
- Pydantic validation
- SQLAlchemy ORM
- Clean dependency injection

## Design choices

**Why single user table?** Easier to manage than separate role tables. Role is just a field.

**Separate endpoints per role?** Clearer access control than checking permissions everywhere.

**Audit Logs?** Care homes need this for compliance.

## Development notes

The system handles real care home scenarios:
- Staff calling in sick (schedule gaps)
- Family wanting updates
- Regulatory inspections (audit trail)
- New resident admissions
- Staff turnover

Built this for an actual care home, so it's not just academic.