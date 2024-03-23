import ast
from datetime import datetime
import os
import json
import asyncio
import re
import time
import importlib

import google.generativeai as genai

# write code to get current time zone

GOOGLE_API_KEY = ""
genai.configure(api_key=GOOGLE_API_KEY)
gemini_pro_model = genai.GenerativeModel('gemini-pro')

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


def parse_json_like_string(text):
    brace_count = 0
    start_index = None
    end_index = None

    for i, char in enumerate(text):
        if char == '{':
            if brace_count == 0:
                start_index = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_index = i + 1  # Include the closing brace
                break

    if start_index is not None and end_index is not None:
        json_string = text[start_index:end_index]
        json_string = json_string.replace("null", "None").replace("false", "False").replace("true", "True")
        json_string = re.sub(r"(\w+)'(\w+)", r"\1^\2", json_string)
        json_string = json_string.replace("'", '"').replace("^", "\'")
        json_data = ast.literal_eval(json_string)
        return json_data
    else:
        raise ValueError("Invalid JSON string")


def convert_msg_format_to_gcp(json_data, prompt="",):
    system_prompt = """
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
    system_prompt = system_prompt + "\n" + prompt + "\nJSON_FORMATE: " + str(json_data)
    list_content_processed = [{'role': 'USER', 'parts': [{'text': system_prompt}]}, ]
    return list_content_processed


def append_to_chat_history(data, chat_history):
    user = {"role": "user", "text": data['user_latest_message']}
    chat_history.append(user)
    if data.get('backend_message'):
        backend = {"role": "backend", "text": data['backend_message']}
        chat_history.append(backend)
    assist = {"role": "assistant", "text": data['assistant_response']}
    chat_history.append(assist)
    return chat_history


def parse_gemini_output(raw_gemini_output, json_data):
    for candidate in raw_gemini_output.candidates:
        string = candidate.content.parts[0].text
        dict_data = parse_json_like_string(string)
        if not dict_data.get("assistant_response"):
            raise ValueError("No response from gemini")
        json_data['chat_history'] = append_to_chat_history(dict_data, json_data.get('chat_history'))
        for field in ["intent", "existing_user", "patient_id", "patient_first_name", "patient_last_name", 
                      "patient_phone_number", "patient_date_of_birth", "flexibility_type", "appointment_reason", 
                      "appointment_date", "appointment_time", "conformation"]:
            if not json_data.get(field) and dict_data.get(field):
                json_data[field] = dict_data.get(field)
        print(dict_data.get("assistant_response"))
    return json_data


def call_gemini_pro(messages, input_json, max_retry_count, model):
    call_count = 0
    while call_count < max_retry_count:
        try:
            response = model.generate_content(contents=messages, stream=False)
            if isinstance(response.text, str):
                output_json = parse_gemini_output(response, input_json)
                return output_json
        except Exception as e:
            error_msg = f"Failed to get GCP LLM response due to -> {str(e)}"
            print(error_msg)
            time.sleep(2)
            call_count += 1
    return input_json


def call_llm(prompt, input_json, model=gemini_pro_model, retry_count=5):
    messages = convert_msg_format_to_gcp(input_json, prompt)
    output_json = call_gemini_pro(messages, input_json, retry_count, model)
    return output_json

# def process_request(json_message):
#     is_call_success = False
#     while not is_call_success:
#         json_message = call_gemini_pro(json_message, 5, gemini_pro_model)
#         json_message['user_latest_message'] = input("Please enter your response here: ")
#     return


# while True:
#     process_request(json_formate)
