from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # API views
    MovieViewSet,
    SeatViewSet,
    BookingViewSet, 

    # template views
    movie_list,
    
)

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('/api', include(router.urls)),             # API lives under /api/
    path('', movie_list, name='movie_list')     # website homepage
]