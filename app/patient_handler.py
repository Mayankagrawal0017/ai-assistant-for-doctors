from db_handler.schemas import PatientUpdate, PatientSchema
from db_handler.models import Patient, get_db
db = get_db()


def create_patient(patient_data):
    patient_data = PatientSchema(**patient_data)
    new_patient = Patient(**patient_data.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


def update_patient(patient_id=None, phone_number=None, patient_data={}):

    if patient_id is not None:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
    elif phone_number is not None:
        patient = db.query(Patient).filter(Patient.phone_number == phone_number).first()
    else:
        raise Exception("No Patient Info")

    if not patient:
        raise Exception("Patient not found")

    patient_data = PatientUpdate(**patient_data)
    for field, value in patient_data.dict(exclude_unset=True).items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient


def get_patient_info(phone_number: str):
    patient = db.query(Patient).filter(Patient.phone_number == phone_number).first()
    return patient


# sample_dict = {
#     "first_name": "John",
#     "last_name": "oe",
#     "date_of_birth": "1980-01-01",
#     "phone_number": "+1234567890"
# }
# create_patient(sample_dict)
# update_patient(patient_id=50, patient_data=sample_dict)
# update_patient(phone_number="+1234567890", patient_data=sample_dict)