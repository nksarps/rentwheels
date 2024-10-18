from .models import Booking
from rest_framework import serializers


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'car', 'start_date', 'end_date', 'currency', 'total_price', 'status']

        read_only_fields = ['id', 'user', 'car', 'currency', 'total_price', 'status']