from django.core.management.base import BaseCommand
from faker import Faker
from halo.models import Class, Booking
from django.utils import timezone
import random 

fake = Faker()

Faker.seed(42)

class Command(BaseCommand):
    help = 'Seed Classes and Bookings with fake data, avoiding duplicates'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting seeding process...")

        #Number of new classes and bookings to create
        NUM_CLASSES = 10
        BOOKINGS_PER_CLASS = 3

        #Create upcoming classes only
        now = timezone.now()

        for _ in range(NUM_CLASSES):
            class_name = fake.word().capitalize()
            instructor = fake.name()

            #atetime in next 30 days
            dt = fake.date_time_between(start_date='now', end_date='+30d', tzinfo=timezone.get_current_timezone())

            slots = random.randint(5, 20)

            #Avoid creating exact duplicate classes (same name + datetime + instructor)
            exists = Class.objects.filter(name=class_name, datetime=dt, instructor=instructor).exists()
            if exists:
                self.stdout.write(f"Skipped duplicate class: {class_name} at {dt}")
                continue

            cls = Class.objects.create(
                name=class_name,
                instructor=instructor,
                datetime=dt,
                slots_available=slots
            )
            self.stdout.write(f"Created Class: {cls}")

            #Seed bookings for this class
            existing_emails = set(
                Booking.objects.filter(class_booked=cls).values_list('client_email', flat=True)
            )

            bookings_created = 0
            attempts = 0
            while bookings_created < BOOKINGS_PER_CLASS and attempts < BOOKINGS_PER_CLASS * 3:
                client_name = fake.name()
                client_email = fake.unique.email()

                #Avoid duplicate emails for bookings globally
                if Booking.objects.filter(client_email=client_email).exists():
                    attempts += 1
                    continue

                #Avoid duplicate email for this class's bookings
                if client_email in existing_emails:
                    attempts += 1
                    continue

                #Create booking
                Booking.objects.create(
                    class_booked=cls,
                    client_name=client_name,
                    client_email=client_email,
                )
                bookings_created += 1
                existing_emails.add(client_email)
                self.stdout.write(f"Created Booking for {client_email} in class {cls.name}")
                attempts += 1

        self.stdout.write(self.style.SUCCESS("Seeding completed!"))        