
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, time
import random

# Import your database models
from models import Doctor, Patient, Appointment

# Database setup
engine = create_engine('sqlite:///AIAD_DB.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Instantiate Faker
fake = Faker()

# Doctor Data
specialities = ['Pediatrician', 'Cardiologist', 'Dermatologist', 'General Physician', 'Dentist']

unique_phone_numbers = set()

while len(unique_phone_numbers) < 5:
    unique_phone_numbers.add(str(fake.random_number(digits=10, fix_len=True)))

for i, phone_number in enumerate(unique_phone_numbers):
    doctor = Doctor(
        name=fake.name(),
        education=fake.sentence(nb_words=8),
        speciality=fake.random_element(elements=specialities),
        phone_number=str(fake.random_number(digits=10, fix_len=True)),
        email=fake.unique.email(),
        working_days=','.join(map(str, random.sample(range(0, 7), 5))),
        slot_duration=random.choice([15, 30, 45, 60])  # Choose a random slot duration

    )
    session.add(doctor)

# Patient Data
while len(unique_phone_numbers) < 50:
    unique_phone_numbers.add(str(fake.random_number(digits=10, fix_len=True)))

for i, phone_number in enumerate(unique_phone_numbers):
    patient = Patient(
        first_name = fake.first_name(),
        last_name = fake.last_name(),
        date_of_birth = fake.date_between(start_date='-80y', end_date='-18y'),
        phone_number = phone_number,
        email=fake.unique.email(),
    )
    session.add(patient)

# Sample Appointment Data (We'll need logic to link with schedules)
for _ in range(100):
    appointment_time = fake.date_between(start_date='today', end_date='+2weeks')
    base_time = time(hour=fake.random_int(min=8, max=10), minute=fake.random_element(elements=(0, 30)))
    # Combine the date and base time
    appointment_datetime = datetime.combine(appointment_time, base_time)
    # Convert to string for storage (optional)
    appointment_timeslot = appointment_datetime.strftime("%H:%M:%p")
    appointment = Appointment(
            patient_id=fake.random_int(min=1, max=50),
            appointment_time=appointment_datetime,
            appointment_timeslot=appointment_timeslot,
            doctor_id=fake.random_int(min=1, max=5),
            remarks=fake.sentence(nb_words=6),
        )
    session.add(appointment)

session.commit()
