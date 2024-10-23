# 🚗 RentWheels

A REST API designed to streamline the processes of managing a car rental company. It's designed to be scalable and provides easy payment integration with **Paystack**


## **Features**
- **User Authentication**: Manage user registrations and logins.
- **Car Listings**: Add, view, update, and delete car listings.
- **Search & Filter**: Find cars based on their make, model, availability, and body type.
- **Bookings**: Rent cars with precise rental periods.
- **Payments**: Integrated with *Paystack* for smooth transactions.
- **Admin Panel**: Manage listings, bookings, payments and users in admin panel.


## **Tech Stack**
- **Backend**: Python (Django Rest Framework)
- **Database**: SQLite3
- **Payment Gateway**: Paystack

## **Getting Started**

### **Prerequisites**
- **Python 3.8+** installed
- **Paystack Account** (for payment integration)

### **Installation**
1. Clone the repository:
```bash
git clone https://github.com/kweku-xvi/rentwheels
```

2. Change directory:
```bash 
cd rentwheels
```

3. Create a virtual environment:
```bash 
python -m venv venv 
source venv/bin/activate # For Linux/macOS
venv\Scripts\activate # For Windows
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Apply migrations:
```bash
python manage.py migrate
```

6. Create super user:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

