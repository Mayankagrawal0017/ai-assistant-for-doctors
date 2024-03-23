from pydantic import BaseModel, Field
from datetime import datetime, date
from enum import Enum


class AppointmentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class AppointmentBase(BaseModel):
    patient_id: int = Field(..., description="ID of the associated patient")
    appointment_time: datetime = Field(..., description="Date of the appointment")
    appointment_timeslot: str = Field(..., description="Time of the appointment (e.g., '10:30 AM')")
    doctor_id: int = Field(..., description="ID of the doctor")
    remarks: str = Field(None, description="Optional remarks")


class AppointmentUpdate(BaseModel):
    appointment_time: datetime = Field(..., description="Date of the appointment")
    appointment_timeslot: str = Field(..., description="Time of the appointment (e.g., '10:30 AM')")


class AppointmentSchema(AppointmentBase):
    # id: int = Field(..., description="Unique ID of the appointment")
    status: AppointmentStatus = Field(default="pending", description="Status of the appointment")

    class Config:
        orm_mode = True  # Allows seamless integration with SQLAlchemy models


class PatientBase(BaseModel):
    first_name: str = Field(..., description="Patient's first name")
    last_name: str = Field(..., description="Patient's last name")
    date_of_birth: date = Field(..., description="Patient's date of birth")
    phone_number: str = Field(..., description="Patient's phone number")
    email: str = Field(..., description="Patient's email")


class PatientUpdate(BaseModel):
    first_name: str = Field(None, description="Update patient's first name")
    last_name: str = Field(None, description="Update patient's last name")
    date_of_birth: date = Field(None, description="Update patient's date of birth")


class PatientSchema(PatientBase):
    # id: int = Field(..., description="Unique ID of the patient")
    class Config:
        orm_mode = True  # Allows seamless integration with SQLAlchemy models
