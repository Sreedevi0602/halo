from rest_framework.response import Response
from rest_framework import status
from halo.models import Booking
import logging

logger = logging.getLogger(__name__)

#Daily booking limit
def check_daily_limit(email, client_tz, today_start_utc, today_end_utc):

    #Enforces daily booking limit for an email
    start = today_start_utc 
    end = today_end_utc

    count = Booking.objects.filter(
        client_email=email,
        booked_at__range=(start, end)
    ).count()

    if count >= 3:
        logger.warning(f"Booking denied for {email}. Exceeded daily booking limit (timezone: {client_tz}).")
        return Response({"error": "You can only book up to 3 classes per day."}, status=status.HTTP_400_BAD_REQUEST)


#Weekly booking limit
def check_weekly_limit(email, client_tz, week_start_utc, week_end_utc):

    #Enforces weekly booking limit for an email
    start = week_start_utc 
    end = week_end_utc

    count = Booking.objects.filter(
        client_email=email,
        booked_at__range=(start, end)
    ).count()

    if count >= 12:
        logger.warning(f"Booking denied for {email}: exceeded weekly booking limit. (timezone: {client_tz}).")
        return Response({"error": "You can only book up to 12 classes per week."}, status=status.HTTP_400_BAD_REQUEST)



#Checks duplicate booking of a class by an email
def has_duplicate_booking(email, cls):

    return Booking.objects.filter(class_booked=cls, client_email=email).exists()
    
    