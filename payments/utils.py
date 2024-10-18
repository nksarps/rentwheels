import os, requests
from dotenv import load_dotenv

load_dotenv()

PAYSTACK_SECRET = os.getenv('PAYSTACK_SECRET')


def initialize_transactions(email:str, amount:str, reference:str, order_id:str):
    url = "https://api.paystack.co/transaction/initialize"

    headers = {
        'authorization': f'Bearer {PAYSTACK_SECRET}'
    }

    data = {
        'email':email,
        'amount':amount,
        'reference':reference,
        'metadata': {
            'order_id':order_id
        }
    }

    response = requests.post(url=url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['data']['authorization_url']
    else:
        return response.json()['message']


