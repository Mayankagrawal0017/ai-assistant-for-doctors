from datetime import datetime

import phonenumbers
from dateutil.parser import parse
from email_validator import validate_email, EmailNotValidError


def verify_email(email):
    try:
        v = validate_email(email)  # validate and get info
        return True
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        return False


def verify_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        if phonenumbers.is_valid_number(parsed_number):
            return True
        else:
            return False
    except phonenumbers.phonenumberutil.NumberParseException:
        return False


def calculate_age(birth_date_str):
    birth_date = datetime.strptime(birth_date_str, '%d%m%Y')
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def fix_date_format(date_str):
    try:
        date = parse(date_str, dayfirst=True).strftime('%d-%m-%Y')
        day, month, year = map(int, date.split('/'))
        if day < 1 or day > 31:
            return False, "Day is invalid. It should be between 1 and 31."
        if month < 1 or month > 12:
            return False, "Month is invalid. It should be between 1 and 12."
        if year < 1900 or year > datetime.now().year:
            return False, "Year is invalid. It should be between 1900 and current year."
        return True, date
    except ValueError:
        return False, "Invalid date format. Please enter date in 'dd/mm/yyyy' format."
