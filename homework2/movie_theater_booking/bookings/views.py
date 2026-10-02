from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import Movie, Seat, Booking 
from .serializers import MovieSerializer, SeatSerializer, BookingSerailizer

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class SeatViewSet(viewsets.ModelViewSet):
        queryset = Seat.objects.all()
        serializer_class = SeatSerializer 

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerailizer


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})

def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    available_seats = Seat.objects.filter(is_booked=False)

    if request.method == 'POST':
        seat_id = request.POST.get('seat')
        seat = get_object_or_404(Seat, id=seat_id)

        # Create the booking, tying together movie + seat + user
        Booking.objects.create(movie=movie, seat=seat, user=request.user)

        # Mark the seat taken so it won't show as available again
        seat.is_booked = True 
        seat.save()

        return redirect('booking_history')
    
    return render(request, 'bookings/seat_booking.html', {
        'movie': movie,
        'available_seats': available_seats,
    })

def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})