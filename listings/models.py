from django.db import models


class Listing(models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]

    RENTAL_STATUS = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintainance', 'Under Maintainance')
    ]

    image = models.ImageField(null=True, blank=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    body_type = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=30, choices=TRANSMISSION_CHOICES)
    status = models.CharField(max_length=20, choices=RENTAL_STATUS, default='available')
    seats = models.PositiveIntegerField()
    doors = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='GHC')
    added_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.year} {self.make} {self.model}'

    
    class Meta:
        ordering = ('-added_at',)



