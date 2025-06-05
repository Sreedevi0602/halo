from django.db import models

# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    slots_available = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} by {self.instructor}'
    
    class Meta:
        ordering = ['datetime']
        verbose_name_plural = "Classes"


class Booking(models.Model):
    class_booked = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField(max_length=200)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_name} booked the {self.class_booked.name} class by {self.class_booked.instructor}'

