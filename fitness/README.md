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

### Seed the data
```cmd
python manage.py seed
```

### Run Tests 

```cmd
python manage.py test halo 
```


---

##  Sample API Requests (Postman Format)

### 1. GET /classes

**Request:**  
`GET http://127.0.0.1:8000/classes/`

**Success Response:**
```json
 [
  {
    "id": 2,
    "datetime": "2025-06-10 08:00 AM",
    "name": "Zumba",
    "instructor": "Kavya Iyer",
    "slots_available": 2
  }
]
```

---

### 2. POST /book

**Request:**
 `POST http://127.0.0.1:8000/book/`
 `Headers: Content-Type: application/json`

```json
 {
  "class_id": 5,
  "client_name": "Hari Krishnan",
  "client_email": "hari@example.com"
}
```

**Success Response:**

```json

{
    "message": "Booking successful",
    "booking": {
        "id": 6,
        "client_name": "Hari Krishnan",
        "client_email": "hari@example.com",
        "booked_at": "2025-06-06T02:03:04.825727Z",
        "class_booked": 5
    }
}
```

**Responses:** Missing Fields:

```json
 { "error": "Missing fields: client_email." }
```

**Responses:** Invalid Name:

```json
 { "error": "Name must contain only letters and spaces." }
```

**Responses:** Invalid Email:

```json
 { "error": "Invalid email format." }
```

**Responses:** Email taken:

```json
 { "error": "This email is already in use. Try with a different one."}
```

**Responses:** No such class exists:

```json
 { "error": "Class not found."}
```

**Responses:** Overbooking:

```json
 { "error": "No slots available." }
```

**Responses:** Daily Limit:

```json
 { "error": "You can only book up to 3 classes per day." }
```

**Responses:** Weekly Limit:

```json
 { "error": "You can only book up to 12 classes per week." }
```

**Responses:** Duplicate:

```json
 { "error": "You have already booked this class." }
```

---

### GET /bookings

**Request:**  

`GET http://127.0.0.1:8000/bookings/?email=rahul@example.com`

**Success Response:**

```json
 [
  {
    "id": 5,
    "class_booked": {
      "id": 4,
      "datetime": "2025-06-05 06:00 AM",
      "name": "Yoga",
      "instructor": "Prachi Sen",
      "slots_available": 2
    },
    "booked_at": "2025-06-05 07:29 PM"
  }
 ]
```

**Missing Email:**

```json
 { "error": "Email is required as a query parameter" }
```

**Invalid Email Format:**

```json
 { "error": "Invalid email format." }
```

**No Bookings:**

```json
 { "error": "No bookings found for this email." }
```


---

## Author

**V S Sreedevi**  
[GitHub: Sreedevi0602](https://github.com/Sreedevi0602)


