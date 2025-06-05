from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Class, Booking
from .serializers import ClassSerializer, BookingSerializer, BookingSummarySerializer
import logging
from rest_framework import status
import re
from datetime import timedelta
from .utils.timezone import get_client_timezone
import pytz


logger = logging.getLogger(__name__)

# Create your views here.
@api_view(['GET'])
def class_list_view(request):
    client_tz = get_client_timezone(request)
    classes = Class.objects.filter(datetime__gte=timezone.now())
    serializer = ClassSerializer(classes, many=True, context={'client_tz': client_tz})
    return Response(serializer.data)


@api_view(['POST'])
def book_class(request):
    data = request.data
    required_fields = ['class_id', 'client_name', 'client_email']
    missing = [f for f in required_fields if not data.get(f)]

    if missing:
        logger.warning(f'Missing fields: {missing}.')
        return Response(
            {"error": f"Missing fields: {',' .join(missing)}."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    class_id = data.get('class_id')
    name = data.get('client_name').strip()
    email = data.get('client_email').strip()

    #Name validation
    if not re.match(r'^[a-zA-Z ]+$', name):
        logger.warning(f"Name validation failed for client_name: '{name}'. Name must contain only letters and spaces.")
        return Response({"error": "Name must contain only letters and spaces."}),

    #Email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        logger.warning(f"Email validation failed for client_email: '{email}'. Invalid email format.")
        return Response({"error": "Invalid email format."}, status=400)
    
    existing = Booking.objects.filter(client_email=email).first()

    if existing and existing.client_name != name:
        logger.warning(f"{email} is already in use by {existing.client_name}. Attempted reuse by {name}.")
        return Response({"error": "This email is already in use. Try with a different one."}, status=400)
    
    try:
        cls = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        logger.error(f"Invalid class_id: {class_id}.")
        return Response({"error": "Class not found."}, status=404)
    
    if cls.slots_available <= 0:
        logger.warning(f"Attempt to overbook class {cls.id}.")
        return Response({"error": "No slots available."}, status=400)
    
    #Get client's timezone
    client_tz = get_client_timezone(request)

    #Get current datetime in UTC and convert to client's timezone
    now_utc = timezone.now()
    now = now_utc.astimezone(client_tz)

    #Calculate start and end of client's local day
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    #Calculate start and end of client's local week
    week_start = today_start - timedelta(days=today_start.weekday())
    week_end = week_start + timedelta(days=7)

    #Convert back to UTC for querying DB
    today_start_utc = today_start.astimezone(pytz.UTC)
    today_end_utc = today_end.astimezone(pytz.UTC)
    week_start_utc = week_start.astimezone(pytz.UTC)
    week_end_utc = week_end.astimezone(pytz.UTC)

    #filter for a day's bookings by this email
    today_bookings = Booking.objects.filter(
        client_email = email,
        booked_at__range = (today_start_utc, today_end_utc)
    )

    #filter for a week's bookings by this email
    weekly_bookings = Booking.objects.filter(
        client_email=email,
        booked_at__range=(week_start_utc, week_end_utc) 
    )

    #Enforce limits (daily=3, weekly=12)
    if today_bookings.count()>= 3:
        logger.warning(f"Booking denied for {email}. Exceeded daily booking limit (timezone: {client_tz}).")
        return Response({"error": "You can only book up to 3 classes per day."}, status=400)
    
    if weekly_bookings.count() >= 12:
        logger.warning(f"Booking denied for {email}: exceeded weekly booking limit. (timezone: {client_tz}).")
        return Response({"error": "You can only book up to 12 classes per week."}, status=400)
    
    if Booking.objects.filter(class_booked=cls, client_email=email).exists():
        logger.info(f"Duplicate booking attempt by {email}.")
        return Response({"error": "You have already booked this class."}, status=400)
    
    booking = Booking.objects.create(
        class_booked=cls,
        client_name=name,
        client_email=email
    )
    cls.slots_available -= 1
    cls.save()

    logger.info(f"Booking created for {email} in {cls.id}.")
    serializer = BookingSerializer(booking)
    return Response({"message": "Booking successful", "booking": serializer.data}, status=201)


@api_view(['GET'])
def get_bookings(request):
    email = request.query_params.get('email')

    if not email:
        logger.warning("Missing email query parameter in GET /bookings request.")
        return Response({"error": "Email is required as a query parameter"}, status=400)
    
    email = email.strip()

    #Email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        logger.warning(f"Email validation failed for {email}. Invalid email format.")
        return Response({"error": "Invalid email format."}, status=400)
    
    logger.info(f"Fetching bookings for {email}.")

    bookings = Booking.objects.filter(client_email=email).order_by('-booked_at') #sorts the bookings in descending order

    if not bookings.exists():
        logger.info(f"No bookings found for {email}.")
        return Response({"error": "No bookings found for this email."}, status=404)
    
    logger.info(f"{bookings.count()} bookings found for {email}")
    client_tz = get_client_timezone(request)
    serializer = BookingSummarySerializer(bookings, many=True, context={'client_tz': client_tz})
    return Response(serializer.data)
