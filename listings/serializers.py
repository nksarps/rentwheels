from .models import Listing
from rest_framework import serializers


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['id', 'make', 'model', 'year', 'body_type', 'fuel_type', 'transmission', 'status', 'seats', 'doors', 'currency', 'price_per_day']

        read_only_fields = ['id']