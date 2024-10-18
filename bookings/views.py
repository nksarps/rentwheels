from .models import Booking
from .serializers import BookingSerializer
from accounts.permissions import IsVerified
from accounts.utils import refund_request_mail
from django.db import transaction
from django.shortcuts import render
from listings.models import Listing
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


def get_car_or_404(id):
    try:
        return Listing.objects.get(id=id)
    except Listing.DoesNotExist:
        return None

def car_not_found_message():
    return Response(
        {
            'success':False,
            'message':'Car not found'
        }, status=status.HTTP_404_NOT_FOUND
    )


@api_view(['POST'])
@permission_classes([IsVerified])
def rent_car(request, id):
    if request.method == 'POST':
        car = get_car_or_404(id=id)
        if not car:
            return car_not_found_message()
        
        if car.status != 'available':
            return Response(
                {
                    'success':False,
                    'message':'This car is not available for rent'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['end_date'] <= serializer.validated_data['start_date']:
                return Response(
                    {
                        'success':False,
                        'message':'End date must be after start date'
                    }, status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(car=car, user=request.user)

            return Response(
                {
                    'success':True,
                    'message':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success':False,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsVerified])
def cancel_booking(request, id):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                booking = Booking.objects.get(id=id)

                if booking.status != 'confirmed':
                    booking.delete()
                    return Response(
                        {
                            'success':False,
                            'message':'Booking canceled successfully'
                        }, status=status.HTTP_400_BAD_REQUEST
                    )
                    
                if request.user != booking.user:
                    return Response(
                        {
                            'success':False,
                            'message':'You do not have the permission to cancel this booking'
                        }, status=status.HTTP_403_FORBIDDEN
                    )

                booking.status = 'canceled'
                booking.save()

                booking.car.status = 'available'
                booking.car.save()

                refund_request_mail(email=booking.user.email, first_name=booking.user.first_name, booking_id=id)

                return Response(
                    {
                        'success':True,
                        'message':'Booking has been successfully canceled. Check your email.'
                    }, status=status.HTTP_200_OK
                )
        except Booking.DoesNotExist as e:
            return Response(
                {
                    'success':False,
                    'message':'Booking does not exist'
                }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'success':False,
                    'error':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )

# GET BOOKINGS BY ID
