from rest_framework import serializers
from .models import Class, Booking

class ClassSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p")
    class Meta:
        model = Class
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = '__all__'


class BookingSummarySerializer(serializers.ModelSerializer):
    class_booked = ClassSerializer(read_only=True)  #Nested serializer for detailed class info
    booked_at = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p")   #Human readable datetime
    
    class Meta:
        model = Booking
        fields = ['id', 'class_booked', 'booked_at']    #Only required fields
        