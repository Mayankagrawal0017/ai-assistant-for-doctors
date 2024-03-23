from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import calender.google_calander_handler as calender_handler
from schemas import (
    AppointmentSchema,
    AppointmentUpdate,
    AppointmentStatus,
    ScheduleBlock,
    ScheduleFree,
)
from models import Appointment, Doctor, Patient, get_db
db_session = get_db()

calendar_service = calender_handler.get_service()


def create_appointment(appointment_data):
    # 1. Validate doctor availability  (You'll still need to implement 'check_doctor_availability')

    # 2. Create appointment record

    appointment = AppointmentSchema(**appointment_data)
    appointment = Appointment(**appointment.dict())

    db_session.add(appointment)
    db_session.commit()  # Assuming your 'db' object has commit functionality
    db_session.refresh(appointment)

    return appointment


def reschedule_appointment(appointment_id: int, new_data: dict):

    appointment = db_session.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise Exception("Appointment not found")

    # Check availability if appointment date/time is being changed

    # Update appointment details
    new_data = AppointmentUpdate(**new_data)
    for field, value in new_data.dict(exclude_unset=True).items():
        setattr(appointment, field, value)

    db_session.commit()
    db_session.refresh(appointment)
    return appointment


def cancel_appointment(appointment_id: int, ):
    appointment = db_session.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise Exception("Appointment not found")

    # Update appointment status to cancelled (optional)
    if appointment.status == AppointmentStatus.pending:
        appointment.status = AppointmentStatus.cancelled
        status, msg = calender_handler.delete_event(calendar_service, appointment.event_id)
        if status:
            db_session.commit()
            return True
    return False


def complete_appointment(appointment_id: int, ):
    appointment = db_session.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise Exception("Appointment not found")

    # Update appointment status to completed
    if appointment.status == AppointmentStatus.pending:
        appointment.status = AppointmentStatus.completed
        db_session.commit()


def list_todays_pending(doctor_id=1):
    today = datetime.now().date()
    appointments = db_session.query(Appointment).filter(Appointment.status == AppointmentStatus.pending,
                                                        func.date(Appointment.appointment_time) == today,
                                                        Appointment.doctor_id == doctor_id).all()
    return [[appointment.id, appointment.appointment_timeslot] for appointment in appointments]


def get_upcoming_appointments(patient_id: int):
    appointments = db_session.query(Appointment).filter(and_(
        Appointment.patient_id == patient_id,
        Appointment.appointment_time > func.now()
    )).all()
    return appointments

# appointment_data = {
#         'patient_id': 13,
#         'appointment_time': datetime.strptime('2024-03-04 10:30 AM', '%Y-%m-%d %I:%M %p'),
#         'appointment_timeslot': '10:30 AM',
#         'doctor_id': 2,
#         'remarks': 'First visit',
#     }
#
# appointment_data_up = {
#     'appointment_time': datetime.strptime('2024-03-05 10:30 AM', '%Y-%m-%d %I:%M %p'),
#     'appointment_timeslot': '10:35 AM',
# }
# create_appointment(appointment_data)
# reschedule_appointment(99, appointment_data)
# cancel_appointment(96)
# complete_appointment(95)



# def check_doctor_availability(doctor_id: int, appointment_date: datetime, appointment_time: str, db: Session) -> bool:
#     conflicting_appointments = db.query(Appointment).filter(
#         Appointment.doctor_id == doctor_id,
#         Appointment.appointment_date == appointment_date,
#         Appointment.appointment_time == appointment_time,
#         Appointment.status != AppointmentStatus.cancelled,
#     ).all()
#     return not conflicting_appointments
