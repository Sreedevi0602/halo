from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Class, Booking
from .serializers import ClassSerializer, BookingSerializer, BookingSummarySerializer
import logging
from rest_framework import status
from .utils.timezone import get_client_timezone
from .utils.validators import is_valid_name ,is_valid_email, is_email_taken
from .utils.time_bounds import get_daily_bounds, get_weekly_bounds
from .utils.booking_limits import check_daily_limit, check_weekly_limit, has_duplicate_booking



logger = logging.getLogger('halo')

# Create your views here.
@api_view(['GET'])
def class_list(request):
    #Get client timezone
    client_tz = get_client_timezone(request)

    #Filter upcoming classes
    now = timezone.now()
    classes = Class.objects.filter(datetime__gte=now)

    if not classes.exists():
        logger.info("No upcoming classes found.")
        return Response({"error": "No upcoming classes available."}, status=status.HTTP_200_OK)
    
    serializer = ClassSerializer(classes, many=True, context={'client_tz': client_tz})
    return Response(serializer.data)


@api_view(['POST'])
def book_class(request):

    #validates required fields in the request data
    data = request.data
    required_fields = ['class_id', 'client_name', 'client_email']
    #If any required field is empty store it to missing variable
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
    if not is_valid_name(name):
        logger.warning(f"Name validation failed for client_name: '{name}'. Name must contain only letters and spaces.")
        return Response({"error": "Name must contain only letters and spaces."}, status=status.HTTP_400_BAD_REQUEST)


    #Email validation
    if not is_valid_email(email):
        logger.warning(f"Email validation failed for client_email: '{email}'. Invalid email format.")
        return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)
    

    #Checks if the email is already taken by a user
    if is_email_taken(email, name):
        logger.warning(f"{email} is already in use . Attempted reuse by {name}.")
        return Response({"error": "This email is already in use. Try with a different one."}, status=status.HTTP_400_BAD_REQUEST)
    
    
    #Checks if a class exists
    try:
        cls = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        logger.error(f"Invalid class_id: {class_id}.")
        return Response({"error": "Class not found."}, status=status.HTTP_404_NOT_FOUND)
    
    
    #Checks if any slot left
    if cls.slots_available <= 0:
        logger.warning(f"Attempt to overbook class {cls.id}.")
        return Response({"error": "No slots available."}, status=status.HTTP_400_BAD_REQUEST)
    

    #Daily and weekly booking bounds
    #Get client's timezone
    client_tz = get_client_timezone(request)

    today_start_utc, today_end_utc = get_daily_bounds(client_tz)
    week_start_utc, week_end_utc = get_weekly_bounds(client_tz)

    #Check daily booking limit
    daily_limit_response = check_daily_limit(email, client_tz, today_start_utc, today_end_utc)
    if daily_limit_response:
        return daily_limit_response
    
    #Check weekly booking limit
    weekly_limit_response = check_weekly_limit(email, client_tz, week_start_utc, week_end_utc)
    if weekly_limit_response:
        return weekly_limit_response


    #Checks duplicate booking of a class by an email
    if has_duplicate_booking(email, cls):
        logger.info(f"Duplicate booking attempt by {email}.")
        return Response({"error": "You have already booked this class."}, status=status.HTTP_400_BAD_REQUEST)
    

    #Reduces available slots upon successful booking
    booking = Booking.objects.create(
        class_booked=cls,
        client_name=name,
        client_email=email
    )
    cls.slots_available -= 1
    cls.save()


    logger.info(f"Booking created for {email} in {cls.id}.")
    serializer = BookingSerializer(booking)
    return Response({"message": "Booking successful", "booking": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_bookings(request):
    email = request.query_params.get('email')

    if not email:
        logger.warning("Missing email query parameter in GET /bookings request.")
        return Response({"error": "Email is required as a query parameter"}, status=status.HTTP_400_BAD_REQUEST)
    

    email = email.strip()

    #Email validation
    if not is_valid_email(email):
        logger.warning(f"Email validation failed for {email}. Invalid email format.")
        return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)
    

    logger.info(f"Fetching bookings for {email}.")

    bookings = Booking.objects.filter(client_email=email).order_by('-booked_at') #sorts the bookings in descending order

    if not bookings.exists():
        logger.info(f"No bookings found for {email}.")
        return Response({"error": "No bookings found for this email."}, status=status.HTTP_404_NOT_FOUND)
    

    logger.info(f"{bookings.count()} bookings found for {email}")
    client_tz = get_client_timezone(request)
    serializer = BookingSummarySerializer(bookings, many=True, context={'client_tz': client_tz})
    return Response(serializer.data)
