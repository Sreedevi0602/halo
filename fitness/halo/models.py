from django.db import models

# Create your models here.
#Represents a fitness class that users can book
class Class(models.Model):
    name = models.CharField(max_length=200) #Name of the class (e.g., Yoga, Pilates)
    datetime = models.DateTimeField()   #Scheduled date and time of the class
    instructor = models.CharField(max_length=100)   #Name of the class instructor
    slots_available = models.PositiveIntegerField() #Number of available booking slots

    def __str__(self):
        return f'{self.name} by {self.instructor}'
    
    class Meta:
        ordering = ['datetime'] #Classes will be ordered by upcoming datetime
        verbose_name_plural = "Classes" #Plural display name in admin panel


#Represents a booking made by a user for a specific class
class Booking(models.Model):
    class_booked = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='bookings')  #The class being booked
    client_name = models.CharField(max_length=100)  #Name of the client
    client_email = models.EmailField(max_length=200)    #Email of the client
    booked_at = models.DateTimeField(auto_now_add=True) #Timestamp when the booking was made

    def __str__(self):
        return f'{self.client_name} booked the {self.class_booked.name} class by {self.class_booked.instructor}'

