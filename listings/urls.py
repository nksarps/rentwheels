from . import views
from django.urls import path


urlpatterns = [
    path('<int:id>', views.get_listing_by_id, name='get_listing_by_id'),
    path('add', views.add_listing, name='add_listing'),
    path('update/<int:id>', views.update_listing, name='update_listing'),
    path('delete/<int:id>', views.delete_listing, name='delete_listing'),
    path('all', views.get_all_listings, name='get_all_listings'),
    path('search', views.search_for_listing, name='search_for_listing'),
    path('filter', views.filter_listings, name='filter_listings'),
]