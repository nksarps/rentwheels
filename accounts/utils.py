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


def generate_id(n:int):
    characters = string.ascii_letters + string.digits
    id_generated = ''.join(random.choices(characters, k=n))

    return id_generated