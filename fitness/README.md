# Halo – Fitness Booking API

A simple Django REST API for booking fitness classes at a fictional studio. Designed to demonstrate backend development skills including API design, validation, error handling, and timezone-aware scheduling.


---

## Project Overview

**Objective:**  
Built a lightweight backend system where clients can view and book fitness classes such as Yoga, Zumba, and HIIT.  
The app handles class scheduling, booking limits, timezone management, and input validation.

This project is part of a backend development evaluation for demonstrating clean code practices, modular design, and proper handling of real-world scenarios like overbooking and duplicate submissions.


---

## Tech Stack

- Python  
- Django  
- Django REST Framework  
- SQLite (in-memory DB)  
- Faker (for data seeding)  
- Pytz (timezone support)
- python-dateutil (for advanced date and time parsing and manipulation)


---

## API Endpoints

### 1. **GET /classes**  
Returns a list of all upcoming fitness classes.

---

### 2. **POST /book**  
Accepts a booking request with:

- `class_id`  
- `client_name`  
- `client_email`  

Includes:

- Booking of different classes for clients  
- Missing fields validation  
- Input validation (name and email)  
- Duplicate email prevention  
- Invalid class detection  
- Duplicate booking prevention  
- Daily booking limit: 3 bookings per day  
- Weekly booking limit: 12 bookings per week  
- Decreases slots on successful booking

---

### 3. **GET /bookings?email=rahul@example.com**
Fetches all bookings made by a specific client email.


---

## Key Features

-  View all upcoming fitness classes
-  Book a class if slots are available
-  Prevent overbooking and duplicates
-  Automatically updates available slots after booking
-  Enforce per-user booking limits (daily & weekly)
-  View all the booked classes by a client as history
-  Timezone management (class times adjusted to client’s local time)
-  Comprehensive logging and error handling
-  Unit tests for core functionalities
-  Modular utils for clean business logic
-  Seed sample data using Faker for testing


---

## How to Run the Project Locally

### Clone the repository

```cmd
git clone <repo url>
cd halo
```

### Create virtual environment

```cmd
pip install virtualenv
virtualenv myenv
myenv\Scripts\activate  # On Windows
```

### Install dependencies

```cmd
pip install django
pip install djangorestframework
pip install pytz
pip install faker
pip install python-dateutil
```

### Setup the database

```cmd
python manage.py makemigrations
python manage.py migrate
```

### Create superuser (optional)

```cmd
python manage.py createsuperuser
```

### Run the server

```cmd
python manage.py runserver
```

## Seed the data
```cmd
python manage.py seed
```

### Run Tests 

```cmd
python manage.py test halo 
```


