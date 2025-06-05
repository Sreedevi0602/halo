from rest_framework import serializers
from .models import Class, Booking
import pytz

class ClassSerializer(serializers.ModelSerializer):
    datetime = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = '__all__'

    def get_datetime(self, obj):
        tz = self.context.get('client_tz', pytz.UTC)
        return obj.datetime.astimezone(tz).strftime("%Y-%m-%d %I:%M %p")


class BookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = '__all__'


class BookingSummarySerializer(serializers.ModelSerializer):
    class_booked = ClassSerializer(read_only=True)  #Nested serializer for detailed class info
    booked_at = serializers.SerializerMethodField()   
    
    class Meta:
        model = Booking
        fields = ['id', 'class_booked', 'booked_at']    #Only required fields

    def get_booked_at(self, obj):
        tz = self.context.get('client_tz', pytz.UTC)
        return obj.booked_at.astimezone(tz).strftime("%Y-%m-%d %I:%M %p")
        