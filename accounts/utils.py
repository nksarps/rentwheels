import os, random, string
from dotenv import load_dotenv
from trycourier import Courier

load_dotenv()

client = Courier(auth_token=os.getenv('COURIER_TOKEN'))

def verify_account_mail(email:str, first_name:str, link:str):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": os.getenv('VERIFICATION_MAIL_TEMPLATE_ID'),
            "data": {
            "appName": "RentWheels",
            "firstName": first_name,
            "link": link,
            },
        }
    )


def password_reset_mail(email:str, first_name:str, link:str):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": os.getenv('PASSWORD_RESET_MAIL_TEMPLATE_ID'),
            "data": {
            "appName": "RentWheels",
            "firstName": first_name,
            "link": link,
            },
        }
    )




def payment_confirmation_mail(email, first_name, currency, amount, make, model, year, paid_at, booking_id, start_date, end_date, transaction_id):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": os.getenv('PAYMENT_CONFIRMED_TEMPLATE_ID'),
            "data": {
            "firstName": first_name,
            "currency": currency,
            "amount": amount,
            "make": make,
            "model": model,
            "year": year,
            "paidAt": paid_at,
            "bookingID": booking_id,
            "startDate": start_date,
            "endDate": end_date,
            "transactionID": transaction_id,
            },
        }
    )


def refund_request_mail(email, first_name, booking_id):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": os.getenv('REFUND_REQUEST_TEMPLATE_ID'),
            "data": {
            "companyName": "RentWheels",
            "firstName": first_name,
            "booking_id": booking_id
            },
        }
    )


def generate_id(n:int):
    characters = string.ascii_letters + string.digits
    id_generated = ''.join(random.choices(characters, k=n))

    return id_generated