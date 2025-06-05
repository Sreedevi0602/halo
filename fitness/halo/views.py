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


logger = logging.getLogger(__name__)

# Create your views here.
@api_view(['GET'])
def class_list_view(request):
    classes = Class.objects.filter(datetime__gte=timezone.now())
    serializer = ClassSerializer(classes, many=True)
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
    
    #Get current datetime
    now = timezone.now()

    #filter for today's bookings by this email
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    today_bookings = Booking.objects.filter(
        client_email = email,
        booked_at__range = (today_start, today_end)
    )

    #filter for a week's bookings by this email
    week_start = now - timedelta(days=now.weekday())
    week_end = week_start + timedelta(days=7)
    weekly_bookings = Booking.objects.filter(
        client_email=email,
        booked_at__range=(week_start, week_end) 
    )

    #Enforce limits
    if today_bookings.exists():
        logger.warning(f"Booking denied for {email}: already booked a class today.")
        return Response({"error": "You have already booked a class today."}, status=400)
    
    if weekly_bookings.count() >= 4:
        logger.warning(f"Booking denied for {email}: exceeded weekly booking limit.")
        return Response({"error": "You can only book up to 4 classes per week. You have exceeded your weekly booking limit."}, status=400)
    
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
    serializer = BookingSummarySerializer(bookings, many=True)
    return Response(serializer.data)
