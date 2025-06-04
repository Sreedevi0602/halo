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

