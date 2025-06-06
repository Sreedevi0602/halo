import re
from halo.models import Booking

#Name validation
def is_valid_name(name):
    return bool(re.match(r'^[a-zA-Z ]+$', name))


#Email validation
def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


#Checks if the email is already taken by a user
def is_email_taken(email: str, name: str) -> bool:

    existing = Booking.objects.filter(client_email=email).first()
    if existing and existing.client_name != name:
        return True