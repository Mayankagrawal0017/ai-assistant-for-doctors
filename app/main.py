# imports
from datetime import datetime

import utils
import patient_handler, appointment_handler


def lambda_handler(data):
    json_data = {
        "current_timestamp": f"This chat started  on {datetime.utcnow().date()} at {datetime.utcnow().time()} and today is {datetime.utcnow().strftime('%A')}",
        "chat_history": [{"role": "system", "text": "start"}],
        "user_latest_message": None,
        "assistant_response": None,
        "backend_message": None,
        "intent": None,
        "verified_user": False,
        "patient_id": None,
        "patient_first_name": None,
        "patient_last_name": None,
        "patient_phone_number": None,
        "patient_date_of_birth": None,
        "flexibility_type": None,
        "appointment_reason": None,
        "appointment_date": None,
        "appointment_time": None,
        "doctor_schedule": {},
        "conformation": False
    }
    json_data_llm = json_data.deepcopy()
    phone_number = data.get('phone_number')
    if not phone_number:
        is_phone_number = False
        while not is_phone_number:
            json_data_llm = {} # call llm to greet user and ask them for their phone number to verify there information is available in the database
            _number = ''   # get the phone number
            status, _number = utils.verify_phone_number(_number)
            if status:
                is_phone_number, phone_number = True, _number

    json_data['patient_phone_number'] = phone_number
    patient = patient_handler.get_patient_info(phone_number)
    if patient.id:
        json_data['verified_user'] = True
        json_data['patient_id'] = patient.id
        json_data['patient_first_name'] = patient.first_name
        json_data['patient_last_name'] = patient.last_name
        json_data['patient_date_of_birth'] = patient.date_of_birth
    else:
        feedback = ''
        while not json_data['verified_user']:
            json_data['backend_message'] = feedback
            # Ask llm to ask user for their information to create their profile also send feedback
            date_of_birth = ''
            status, feedback = utils.fix_date_format(date_of_birth)
            patient_object = {
              'first_name': '',
              'last_name': '',
              'date_of_birth': date_of_birth,
              'email': '',
              'phone_number': json_data['patient_phone_number']
            }

            # create patient
            new_patient = patient_handler.create_patient(patient_object)
            if new_patient.id:
                json_data['verified_user'] = True
                json_data['patient_id'] = new_patient.id
                json_data['patient_first_name'] = new_patient.first_name
                json_data['patient_last_name'] = new_patient.last_name
                json_data['patient_date_of_birth'] = new_patient.date_of_birth

    if json_data['verified_user']:
        # check for intent

        if not json_data.get('intent'):
            pass
        if json_data.get('intent') != 'book':
            while not json_data['conformation']:
                appointments = appointment_handler.get_upcoming_appointments(json_data['patient_id'])
                # send info for confirmation
                # if not then send information all upcoming appointment information and ask them to choose
                # send info for confirmation
                _appointment = ''

                status = appointment_handler.cancel_appointment(_appointment['id'])
                if json_data.get('intent') == 'reschedule':
                    # change intent to book
                    pass
                else:
                    # send info that is appointment  cancelled
                    pass
                pass

        if json_data.get('intent') == 'book':
            feedback = ''
            while not json_data['conformation']:
                # check for info already there in for the appointment
                # create feedback based what else we need
                # extract reason
                # extract doctors name  if not present provide them options based on reasons and ask them to choose
                # extract date and time from the appointment
                # check calendar if it's available
                # if not get next best option ask  them to provide flexibility type
                # get 3 next best option based flexibility
                # if not get loop
                pass

        pass


if __name__ == '__main__':
    data = {'phone_number': "4080461135"}
    lambda_handler(data)
