from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


#Single user table
class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # admin manager carer or family


    name = Column(String, nullable=True)  # All except admin
    phone = Column(String, nullable=True)  # carer, family only
    department = Column(String, nullable=True)  # manager only
    family_id = Column(String, nullable=True)  # family only

    # Relationships
    schedules = relationship("Schedule", back_populates="carer")
    assigned_clients = relationship("Client", secondary="assignments", back_populates="assigned_users")



#Assignments table

assignments = Table(
    'assignments',
    Base.metadata,
    Column('user_email', String, ForeignKey('users.email', ondelete='CASCADE'), primary_key=True),
    Column('client_id', String, ForeignKey('clients.id', ondelete='CASCADE'), primary_key=True)
)




#Client Table

class Client(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    room = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False)
    support_needs = Column(Text, nullable=False)

    # Simple relationships
    assigned_users = relationship("User", secondary=assignments, back_populates="assigned_clients")
    visit_logs = relationship("VisitLog", back_populates="client")
    schedules = relationship("Schedule", back_populates="client")





#Schedule Table
class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(String, primary_key=True, index=True)
    carer_email = Column(String, ForeignKey('users.email'), nullable=False)
    client_id = Column(String, ForeignKey('clients.id'), nullable=False)
    date = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    shift_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="scheduled")
    notes = Column(Text)
    completed_at = Column(String)


    carer = relationship("User", back_populates="schedules")
    client = relationship("Client", back_populates="schedules")





#Visit Log table

class VisitLog(Base):
    __tablename__ = "visit_logs"

    id = Column(String, primary_key=True, index=True)
    client_id = Column(String, ForeignKey('clients.id'), nullable=False)
    carer_name = Column(String, nullable=False)
    carer_number = Column(String)
    date = Column(DateTime, nullable=False)
    personal_care_completed = Column(Boolean, nullable=False)
    care_reminders_provided = Column(Text, nullable=False)
    toilet = Column(Boolean, nullable=False)
    changed_clothes = Column(Boolean, nullable=False)
    ate_food = Column(Text, nullable=False)
    notes = Column(Text, nullable=False)
    mood = Column(JSON)
    last_updated_by = Column(String)
    last_updated_at = Column(DateTime)

    client = relationship("Client", back_populates="visit_logs")



# Audit Logs

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String, nullable=False)
    action = Column(String, nullable=False)  # e.g created_visit_log
    entity_type = Column(String, nullable=False)  # e.g visit_log
    entity_id = Column(String, nullable=False)  # The ID of what was changed
    timestamp = Column(DateTime, default=datetime.utcnow)

