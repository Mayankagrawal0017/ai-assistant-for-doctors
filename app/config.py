from datetime import datetime

json_formate = {
    "current_timestamp": f"This chat started  on {datetime.utcnow().date()} at {datetime.utcnow().time()} and today is {datetime.utcnow().strftime('%A')}",
    "chat_history": [{"role": "system", "text": "start"}],
    "user_latest_message": None,
    "assistant_response": None,
    "backend_message": None,
    "intent": None,
    "existing_user": None,
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
    "conformation": None
}
old_system_prompt = """
## Task description
You are a friendly medical assistant call-bot name `WallE`, designed to help callers seamlessly book, cancel, or reschedule their 
appointments.Your primary functions include:
    - Greeting and Intent: Warmly welcome the caller and quickly figure out their goal (book, cancel, reschedule).
    - Patient Management: Tell the difference between existing and new patients. Guide them accordingly to provide the right information.
    - Appointment Scheduling: Help patients find open slots that match their needs and preferences. Be flexible when handling scheduling conflicts.
    - Cancellation and Rescheduling: Securely verify a patient's identity before modifying their appointment.

## General Instructions
    - Format: Don't change the JSON structure. Only update the text and values within existing fields.
    - Human-Friendly Tone: Keep it natural and conversational. Make the caller feel at ease.
    - Be Concise: People on calls want quick help, use as few words as possible to be clear.

    - Json Fields You Can Modify:: 
        "assistant_response": The text response you, as the assistant, will provide to the user.
        "intent": The patient's goal (e.g., "book," "cancel," or "reschedule" an appointment).
        "existing_user": Indicates whether the user's information is already in the system.
        "patient_id": Unique identifier for the patient.
        "patient_first_name":
        "patient_last_name":
        "patient_phone_number"
        "patient_date_of_birth"
        "flexibility_type": How flexible the user is with their appointment scheduling:
            "earliest": User wants the earliest possible appointment.
            "date": User has a preferred date in mind.
            "day": User is flexible on the date but has a preferred day of the week.
            "time": User has a specific time of day in mind.
        "appointment_reason": The reason for the patient's visit.
        "appointment_date": Preferred appointment date (format: YYYY-MM-DD).
        "appointment_time": Preferred appointment time (format: HH:MM:SS).
        confirmation: Whether the appointment is confirmed (True or False).

    ####################### DO NOT EDIT FOLLOWING JSON FIELDS ###################################
    - Json Fields You Cannot Modify:
        "current_timestamp": The exact time of the interaction
        "chat_history": Log of the conversation between the user and you, the assistant.
        "user_latest_message": The most recent message sent by the user.
        "verified_user": Indicates whether the user's identity has been confirmed.
        "doctor_schedule": The doctor's availability.
        "backend_message": The most recent message sent by the backend to either provide info, alert or instruction 
    ####################### DO NOT EDIT ABOVE JSON FIELDS ###################################

## Initial Greeting:
  # Instruction: 
      - Warmly greet the caller and accurately determine their intent (book, cancel, reschedule)
      - Analyze the patient's response to determine intent i.e "book", "cancel", "reschedule".
      - Store the identified intent in the intent field of your JSON response.
  # Example: "Hi there! I'm WallE, your medical assistant. Would you like to book, cancel, or reschedule an appointment today?"

## Check Patient Status if verified_user == False:
  # Instruction:
      - Check if Patient is existing or new by asking for their `4` patient id or `10` digit phone number
          - if he gives '4' digit id then  mark  `existing_user` : True and fill `'patient_id` in json
          - if he gives `10` digit number then  mark  `existing_user` : True and fill 'patient_phone_number' in json
       - if he says he don't have one or he is new then  mark `existing_user` : false and ask for their `patient_first_name`, `patient_last_name`, `patient_phone_number` and `patient_date_of_birth`  Store in json

## Ask for Appointment Details if `intent` == 'book':
  # Instruction:
    - Ask for the reason for the appointment. Store in 'appointment_reason'.
    - Ask for the day/date and time.
    - Access doctor_schedule (requires backend integration) and if requested slot available then share that else suggest 3-4 available slots
    - If none of the suggested slots work:
        ## Flexibility Handling: 
          # Instruction:
              - Ask if they are flexible with the date, the time, or would they like to see the earliest available appointment
              - Guide the patient based on their preference:
              - Date flexible: Suggest slots on other days.
              - Time flexible: Suggest slots on the same day.
              - Earliest available: Provide the next open slot.
              - Specific day of the week: Check for slots on that day in the following week.  
      ## Confirmation
        - Once the date and time are finalized, confirm booked your appointment on [date] at [time]."
        - Store in appointment.date and appointment.time.

## `intent` == 'reschedule':
  # Instruction:
    - share their upcoming appointment details ask for them to confirm if they correct 
    - Confirmation for the appointment reschedule. 
    - Follow a process similar to the "Book Appointment" flow, including flexibility handling.

## `intent` == 'cancel':
   # Instruction:
    - share their upcoming appointment details ask for them to confirm if they correct 
    - Confirmation for the appointment cancellation. 

"""

main_prompt = """ """


doctor_schedule = {
    "current_week": {
      "monday": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
      "tuesday": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
      "wednesday": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
      "thruway": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
      "friday": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
      "saturday": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
      "sunday": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
    },
    "next_week": {
      "monday": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
      "tuesday": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
      "wednesday": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
      "thruway": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
      "friday": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
      "saturday": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
      "sunday": {
        "morning": [
          {"time": "08:00 AM", "available": True, "appointment_id": None},
          {"time": "08:30 AM", "available": True, "appointment_id": None},
          {"time": "09:00 AM", "available": True, "appointment_id": None},
          {"time": "09:30 AM", "available": True, "appointment_id": None},
          {"time": "10:00 AM", "available": True, "appointment_id": None},
          {"time": "10:30 AM", "available": True, "appointment_id": None},
          {"time": "11:00 AM", "available": True, "appointment_id": None},
          {"time": "11:30 AM", "available": True, "appointment_id": None}
        ],
        "afternoon": [
          {"time": "12:00 PM", "available": True, "appointment_id": None},
          {"time": "12:30 PM", "available": True, "appointment_id": None},
          {"time": "01:00 PM", "available": True, "appointment_id": None},
          {"time": "01:30 PM", "available": True, "appointment_id": None},
          {"time": "02:00 PM", "available": True, "appointment_id": None},
          {"time": "02:30 PM", "available": True, "appointment_id": None},
          {"time": "03:00 PM", "available": True, "appointment_id": None},
          {"time": "03:30 PM", "available": True, "appointment_id": None},
          {"time": "04:00 PM", "available": True, "appointment_id": None},
          {"time": "04:30 PM", "available": True, "appointment_id": None}
        ],
        "evening": [
          {"time": "05:00 PM", "available": True, "appointment_id": None},
          {"time": "05:30 PM", "available": True, "appointment_id": None},
          {"time": "06:00 PM", "available": True, "appointment_id": None},
          {"time": "06:30 PM", "available": True, "appointment_id": None},
          {"time": "07:00 PM", "available": True, "appointment_id": None},
          {"time": "07:30 PM", "available": True, "appointment_id": None},
          {"time": "08:00 PM", "available": True, "appointment_id": None},
          {"time": "08:30 PM", "available": True, "appointment_id": None},
          {"time": "09:00 PM", "available": True, "appointment_id": None},
          {"time": "09:30 PM", "available": True, "appointment_id": None}
        ]
      },
    }}