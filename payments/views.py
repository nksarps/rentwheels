import json
from .models import Payment
from .utils import initialize_transactions
from accounts.models import User
from accounts.permissions import IsVerified
from accounts.utils import generate_id, payment_confirmation_mail
from bookings.models import Booking
from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


def get_booking_or_404(id):
    try:
        return Booking.objects.get(id=id)
    except Booking.DoesNotExist:
        return None

def booking_not_found_message():
    return Response(
        {
            'success':False,
            'message':'Booking does not exist'
        }, status=status.HTTP_404_NOT_FOUND
    )


@api_view(['POST'])
@permission_classes([IsVerified])
def checkout(request, id):
    if request.method == 'POST':
        email = request.user.email

        booking = get_booking_or_404(id)
        if not booking:
            return booking_not_found_message()

        amount = str(100 * booking.total_price)
        transaction = initialize_transactions(email=email, amount=amount, reference=generate_id(20), order_id=id)

        return Response(
            {
                'success':True,
                'message':'Authorization URL created!',
                'authorization_url':transaction
            }, status=status.HTTP_200_OK
        )


@api_view(['POST'])
def payment_webhook(request):
    if request.method == 'POST':
        payload = json.loads(request.body)

        event = payload['event']
        data = payload['data']
        user = User.objects.get(email=data['customer']['email'])

        if event == 'charge.success':
            reference = data['reference']
            booking_id = data['metadata']['order_id']

            try:
                with transaction.atomic():
                    booking = get_booking_or_404(booking_id)
                    if not booking:
                        return booking_not_found_message
                        
                    booking.status = 'confirmed'
                    booking.car.status = 'rented'
                    booking.car.save()
                    booking.save()


                    Payment.objects.create(booking=booking, user=user, amount=(data['amount']/100), paid_at=data['paid_at'])

                    payment_confirmation_mail(email=data['customer']['email'], first_name=booking.user.first_name, 
                        currency=data['currency'], amount=(data['amount'] / 100), 
                        make=booking.car.make, model=booking.car.model, 
                        year=booking.car.year, paid_at=data['paid_at'], 
                        booking_id=booking_id, start_date=str(booking.start_date), 
                        end_date=str(booking.end_date), transaction_id=reference
                    )
            except Exception as e:
                return Response(
                    {
                        'success':False,
                        'message':str(e)
                    }, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {
                'success':True,
                'reference':reference
            }, status=status.HTTP_200_OK
        )