# 🏋️ Halo – Fitness Booking API

A simple Django REST API for booking fitness classes at a fictional studio. Designed to demonstrate backend development skills including API design, validation, error handling, and timezone-aware scheduling.

---

## 📋 Project Overview

**Objective:**  
Built a lightweight backend system where clients can view and book fitness classes such as Yoga, Zumba, and HIIT.  
The app handles class scheduling, booking limits, timezone management, and input validation.

This project is part of a backend development evaluation for demonstrating clean code practices, modular design, and proper handling of real-world scenarios like overbooking and duplicate submissions.

---

## 🛠 Tech Stack

- Python  
- Django  
- Django REST Framework  
- SQLite (in-memory DB)  
- Faker (for data seeding)  
- Pytz (timezone support)

---

## 🔌 API Endpoints

### 1. `GET /classes`  
Returns a list of all upcoming fitness classes.

---

### 2. `POST /book`  
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

### 3. `GET /bookings?email=rahul@example.com`  
Fetches all bookings made by a specific client email.

---

## ⭐ Key Features

- View all upcoming fitness classes  
- Book a class if slots are available  
- Prevent overbooking and duplicates  
- Automatically update client slots on successful booking  
- Enforce per-user booking limits (daily & weekly)  
- View booking history by client  
- Timezone-aware class scheduling  
- Comprehensive logging and error handling  
- Unit tests for core functionalities  
- Modular `utils.py` for clean business logic  
- Seed sample data using `Faker`

---

## 🛠️ How to Run the Project Locally

### Clone the repository

```bash
git clone <repo-url>
cd halo
