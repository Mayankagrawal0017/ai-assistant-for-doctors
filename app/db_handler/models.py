import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Database setup
engine = create_engine('sqlite:///AIAD_DB.db', echo=True)  # Connect to SQLite
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Session()
    return db


class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    education = Column(String)
    speciality = Column(String)
    email = Column(String, nullable=False)  # Column to store a reference to the JSON schedule (e.g., filename)
    slot_duration = Column(Integer, nullable=False)
    phone_number = Column(String(20), nullable=False)
    working_days = Column(String)  # Store working days as string
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


# Patient Model
class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


# Appointment Model
class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    event_id = Column(String, nullable=False)
    appointment_time = Column(DateTime, nullable=False)
    appointment_timeslot = Column(String(10), nullable=False)  # Store like '10:30 AM'
    doctor_id = Column(Integer, nullable=False)
    remarks = Column(String)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    status = Column(String(20), nullable=False, default='pending')

# Base.metadata.create_all(engine)
