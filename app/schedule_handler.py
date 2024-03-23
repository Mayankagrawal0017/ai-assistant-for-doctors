from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import json
from datetime import datetime, date, timedelta

schedule_router = APIRouter(prefix="/schedule")


def update_doctor_schedule(schedule_file, doctor_id, week, days=[], time_slot=None, block_week=False):
    with open(schedule_file, 'r') as f:
        schedule_data = json.load(f)

    schedule = schedule_data.get(doctor_id)
    if schedule is None:
        return []

    if days:
        for day in days:
            _update_schedule_slot(schedule[week][day.lower()], time_slot, block=True)

    elif block_week and time_slot:
        for day_of_week in schedule[week]:
            _update_schedule_slot(schedule[week][day_of_week], time_slot, block=True)

    return schedule


def _update_schedule_slot(day_schedule, time_slot, block):
    """Helper function to update a single time slot or full day."""
    if time_slot:
        for slot in day_schedule['morning'] + day_schedule['afternoon'] + day_schedule['evening']:
            if slot['time'] == time_slot:
                slot['available'] = not block
                slot['appointment_id'] = "Doctor" if block else None  # Assuming 'Doctor' indicates blocked
    else:
        for slot in day_schedule['morning'] + day_schedule['afternoon'] + day_schedule['evening']:
            slot['available'] = not block
            slot['appointment_id'] = "Doctor" if block else None


def get_available_slots(schedule_file, doctor_id, appointment_date, requested_datetime, flexibility):
    with open(schedule_file, 'r') as f:
        schedule_data = json.load(f)

    doctor_schedule = schedule_data.get(doctor_id)
    if doctor_schedule is None:
        return []  # Doctor not found

    available_slots = []
    # 1. Check requested slot
    slot_key = get_slot_key(requested_datetime)
    if slot_key in get_slots_for_day(doctor_schedule, requested_datetime) and doctor_schedule[slot_key]['available']:
        available_slots.append(requested_datetime.strftime('%Y-%m-%d %H:%M'))

    # 2. Flexibility levels
    if flexibility == 'on_time':
        available_slots += find_requested_time_next_day(doctor_schedule, requested_datetime)
    elif flexibility == 'on_date':
        available_slots += find_other_slots_on_date(doctor_schedule, appointment_date)
    elif flexibility == 'on_week':
        available_slots += find_other_slots_on_week(doctor_schedule, appointment_date)

    return available_slots


# Helper functions
def get_slot_key(dt):
    day_of_week = dt.strftime('%A').lower()
    time_of_day = get_time_of_day(dt)
    return f"current_week.{day_of_week}.{time_of_day}"


def get_time_of_day(dt):
    hour = dt.hour
    if 8 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    else:
        return "evening"


def get_slots_for_day(doctor_schedule, date_obj):
    day_of_week = date_obj.strftime('%A').lower()
    return doctor_schedule['current_week'][day_of_week]


def find_next_on_same_day(doctor_schedule, requested_datetime):
    slots = get_slots_for_day(doctor_schedule, requested_datetime.date())
    slot_key = get_slot_key(requested_datetime)
    current_index = slots.index(slot_key)

    available = []
    for slot in slots[current_index + 1:]:  # Check slots after the requested time
        if slot['available']:
            available.append(datetime.combine(requested_datetime.date(), datetime.strptime(slot['time'], '%H:%M').time()).strftime('%Y-%m-%d %H:%M'))
    return available


def find_other_slots_on_date(doctor_schedule, appointment_date):
    slots = get_slots_for_day(doctor_schedule, appointment_date)
    available = []
    for slot in slots:
        if slot['available']:
            available.append(datetime.combine(appointment_date, datetime.strptime(slot['time'], '%H:%M').time()).strftime('%Y-%m-%d %H:%M'))
    return available


def find_requested_time_next_day(doctor_schedule, requested_datetime):
    next_day = requested_datetime.date() + timedelta(days=1)
    while next_day.weekday() >= 5:  # Skip weekends if necessary
        next_day += timedelta(days=1)

    slot_key = get_slot_key(requested_datetime)
    if slot_key in get_slots_for_day(doctor_schedule, next_day) and doctor_schedule[slot_key]['available']:
        return [datetime.combine(next_day, datetime.strptime(slot_key['time'], '%H:%M').time()).strftime('%Y-%m-%d %H:%M')]
    else:
        return []


def find_other_slots_on_week(doctor_schedule, appointment_date):
    available_slots = []
    start_date = appointment_date - timedelta(days=appointment_date.weekday())  # Start of the week
    end_date = start_date + timedelta(days=6)  # End of the week

    current_date = start_date
    while current_date <= end_date:
        slots = get_slots_for_day(doctor_schedule, current_date)
        for slot in slots:
            if slot['available']:
                available_slots.append(datetime.combine(current_date, datetime.strptime(slot['time'], '%H:%M').time()).strftime('%Y-%m-%d %H:%M'))
        current_date += timedelta(days=1)

    return available_slots



