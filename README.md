# CareView - Care Home Management System

A care home management system designed for professional healthcare facilities with digital care
tracking and staff coordination. The system uses a PostgreSQL database for data storage,
FastAPI backend for REST API routes, and role-based authentication to ensure the correct access level for certain users.


# Visit the Site
https://careview-backend-production.up.railway.app


## 🎥 Demo Video
[![CareView Demo](https://img.shields.io/badge/▶️_Watch_Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=V78btCnI87Y)



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


## Tech Stack

- **Backend**: FastAPI + PostgreSQL 
- **Auth**: JWT tokens, password hashing
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
- Single user table with roles 
- Many-to-many carer/client assignments  
- Audit logging for creating and deleting entitys
- Schedule conflict prevention

### Security
- JWT auth (8 hour expiry)
- password hashing
- Input validation
- Role-based access control
- Audit logs

### API structure
- FastAPI
- Pydantic validation and models
- Clean dependency injections for role based access



## Development notes
Built this for an actual care home, so it's not just academic.
