from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import Movie, Seat, Booking 
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer 

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})

def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        seat_ids = request.POST.getlist('seats')    # a LIST now, not one value
        booked, skipped = [], []

        for seat_id in seat_ids:
            # Re-check availability on the server - never trust the client.
            try:
                seat = Seat.objects.filter(id=seat_id, is_booked=False).first()
            except (ValueError, TypeError):
                skipped.append(seat_id)
                continue
            if seat is None:        # doesn't exist, or already taken
                skipped.append(seat_id)
                continue
            
            Booking.objects.create(movie=movie, seat=seat, user=request.user)
            seat.is_booked = True 
            seat.save()
            booked.append(seat.seat_number)

        if booked:
            messages.success(request, f"Booked {len(booked)} seat(s): {', '.join(booked)}")
        if skipped:
            messages.warning(request, f"{len(skipped)} seat(s): {', '.join(skipped)} were already taken and skipped.")
        return redirect('booking_history')

    # GET: fetch ALL seats and group them by row letter for the grid.
    seats = Seat.objects.all().order_by('seat_number')     # A1 ... A8, B1 ... B8, etc.
    rows = {}
    for seat in seats:
        rows.setdefault(seat.seat_number[0], []).append(seat)
    seat_rows = sorted(rows.items())        # [('A', [1-8]), ('B', [1-8]) ...]

    return render(request, 'bookings/seat_booking.html', {
        'movie': movie,
        'seat_rows': seat_rows,
    })

def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})