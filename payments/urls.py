from . import views
from django.urls import path


urlpatterns = [
    path('checkout/<str:id>', views.checkout, name='checkout'),
    path('webhook', views.payment_webhook, name='payment_webhook'),
]