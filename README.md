# CareView - Care Home Management System

A comprehensive care home management system designed for professional healthcare facilities with digital care tracking and staff coordination. The system utilizes a PostgreSQL database for secure healthcare data storage, FastAPI backend for robust REST API services, and role-based authentication to ensure compliant access control.

## Demo Accounts
Experience the system with these demo accounts or use the 'demo mode' feature on the website:
- **Manager**: `manager@demo.com` / `password123`
- **Carer**: `carer@demo.com` / `password123`
- **Family**: `family@demo.com` / `password123`

## Core Features

- **PostgreSQL Database:** Securely stores resident information, care logs, staff schedules, and comprehensive audit trails for compliance.
- **FastAPI Backend:** Provides a high-performance RESTful API with automatic documentation, JWT authentication, and healthcare-grade security measures.
- **Role-Based Access Control:** Ensures managers, carers, and family members only access appropriate information with comprehensive permission management.
- **Digital Care Logging:** Real-time visit documentation with mood tracking, medication records, and detailed care notes for each resident.
- **Staff Scheduling:** Complete shift management system with status tracking and conflict prevention for care continuity.
- **Audit Trail:** Full activity logging for regulatory compliance and care quality assurance.

## System Capabilities

This system demonstrates real-world care home workflows including:
- Complete resident care profiles and staff assignments
- Staff scheduling with conflict prevention and shift management
- Digital visit logging and comprehensive care documentation
- Family access to care updates and upcoming schedules
- Manager oversight with dashboard analytics and audit trails

## Prerequisites

Before running this project locally, ensure you have:
- Python 3.8 or higher
- PostgreSQL database
- Git
- Virtual environment tool (venv or conda)

## Installation

### Backend Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/careview-system.git
   cd careview-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv careview-env
   source careview-env/bin/activate  # On Windows: careview-env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   # Create .env file with your database credentials
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=careview
   DB_USER=your_username
   DB_PASSWORD=your_password
   SECRET_KEY=your_jwt_secret_key
   ```

5. Initialize the database with sample data:
   ```bash
   python reset.py
   ```

6. Run the FastAPI application:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Usage

- **API Documentation:** Access interactive API docs at `http://localhost:8000/docs`
- **Health Check:** Monitor system status at `http://localhost:8000/health`
- **System Status:** View database and application metrics at `http://localhost:8000/status`

### Core API Endpoints

- **Authentication:**
  - `POST /login` - User authentication with JWT token generation
  - `GET /me` - Current user profile and permissions

- **Manager Operations:**
  - `GET /manager/clients` - Complete resident management (CRUD)
  - `GET /manager/carers` - Staff account management and assignments
  - `GET /manager/schedules` - Shift scheduling and coordination
  - `GET /manager/dashboard` - Real-time facility overview

- **Carer Operations:**
  - `GET /carer/me/clients` - Assigned resident information
  - `GET /carer/me/schedules` - Personal shift management
  - `POST /carer/me/clients/{id}/visit-log` - Digital care documentation

- **Family Access:**
  - `GET /family/me/clients` - Family member care information
  - `GET /family/me/schedules` - Upcoming care appointments
  - `GET /family/me/today` - Daily care summary and updates

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

Test coverage includes:
- Authentication and authorization flows
- Role-based access control validation
- CRUD operations for all entities
- Error handling and edge cases
- Healthcare data security compliance

## Technical Architecture

### Database Design
- **Single User Table:** Unified user management with role-based differentiation
- **Many-to-Many Assignments:** Flexible carer-client relationships
- **Audit Logging:** Complete activity tracking for compliance
- **Schedule Conflict Prevention:** Automated validation to prevent double-booking

### Security Features
- **JWT Authentication** with 8-hour token expiry for healthcare security
- **bcrypt Password Hashing** with salt for secure credential storage
- **Input Validation** preventing SQL injection and data corruption
- **Audit Logging** for all critical operations and data modifications
- **Role-Based Permissions** ensuring compliant data access

### API Design
- **FastAPI Framework** with automatic OpenAPI documentation
- **Pydantic Models** for request/response validation
- **SQLAlchemy ORM** for database interactions
- **Dependency Injection** for clean authentication flow



## Key Design Decisions

- **Single User Table:** Chose unified user management over separate role tables for simplicity and maintainability
- **String-based IDs:** Used readable identifiers (CL001, SCH001) for easier debugging and logs
- **Role-based Routes:** Separated endpoints by user role for clear access control
- **Audit Trail:** Implemented comprehensive logging for healthcare compliance requirements

## Contributing

Contributions are welcome! This project follows healthcare software development standards:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/care-improvement`)
3. Ensure all tests pass
4. Submit a pull request with detailed change documentation

For bug reports or feature requests, please open an issue with:
- Clear problem description
- Steps to reproduce
- Expected vs actual behavior
- System environment details

## License

This project is developed for educational and demonstration purposes. For production healthcare use, ensure compliance with local healthcare regulations and data protection laws.