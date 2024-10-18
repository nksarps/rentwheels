import uuid
from accounts.models import User
from bookings.models import Booking
from django.db import models


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField()


    def __str__(self):
        return f'Payment by {self.user.username} for booking, {self.booking.id}'


    class Meta:
        ordering = ('-paid_at',)
