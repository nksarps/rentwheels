from . import views
from django.urls import path


urlpatterns = [
    path('rent/<int:id>', views.rent_car, name='rent_car'),
    path('cancel/<str:id>', views.cancel_booking, name='cancel_booking'),
]