from . import views
from django.urls import path


urlpatterns = [
    path('signup', views.signup, name='sign_up'),
    path('verify-user', views.verify_user, name='verify_user'),
    path('login', views.login, name='login'),
    path('password-reset', views.password_reset, name='password_reset'),
    path('password-reset-confirm', views.password_reset_confirm, name='password_reset_confirm'),
    path('user/<str:id>', views.get_user_by_id, name='get_user_by_id'),
]