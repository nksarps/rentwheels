import uuid
from accounts.models import User
from listings.models import Listing
from django.core.exceptions import ValidationError
from django.db import models


class Booking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled')
    ]

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Listing, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    currency = models.CharField(max_length=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.car}'

    
    def save(self, *args, **kwargs):
        rental_days = (self.end_date - self.start_date).days
        self.total_price = rental_days * self.car.price_per_day

        self.currency = self.car.currency

        super().save(*args, **kwargs)


    class Meta:
        ordering = ('-created_at',)