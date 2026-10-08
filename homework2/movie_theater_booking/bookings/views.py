from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from .models import Movie, Seat, Booking 
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

# ---------- API views (DRF) ----------
# Each ModelViewSet provides full CRUD (list/create/retrieve/update/delete);
# the router in urls.py exposes them under /api/.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer 

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# ---------- Template views (website) ----------

# Homepage: lists every movie. Public, no login needed.
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})

# GET shows the seat map for one movie; POST books the selected seats.
# login_required sends anonymous users to LOGIN_URL (the admin login page).
@login_required
def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        # getlist() because the form sends one hidden 'seats' input per selected seat
        seat_ids = request.POST.getlist('seats')
        booked, skipped = [], []

        for seat_id in seat_ids:
            seat = Seat.objects.filter(id=seat_id).first()
            # Unknown seat id (e.g. tampered form) - skip it rather than 404 the whole request
            if seat is None:
                skipped.append(str(seat_id))
                continue
            # Taken only if a Booking already exists for THIS seat AND THIS movie
            already = Booking.objects.filter(movie=movie, seat=seat).exists()
            if already:
                skipped.append(seat.seat_number)
                continue
            
            Booking.objects.create(movie=movie, seat=seat, user=request.user)
            booked.append(seat.seat_number)

        if booked:
            messages.success(request, f"Booked {len(booked)} seat(s): {', '.join(booked)}")
        # Note: skipped also includes invalid seat ids, not only taken seats
        if skipped:
            messages.warning(request, f"{len(skipped)} seat(s): {', '.join(skipped)} were already taken and skipped.")
        return redirect('booking_history')

    # GET: fetch ALL seats and group them by row letter for the grid.
    # String sort: A1 ... A8, B1 ... B8 works for the seeded 1-8 seats, but
    # double-digit seats would sort out of order (e.g. "A10" before "A2").
    seats = Seat.objects.all().order_by('seat_number')
    # Seats taken for THIS movie only; a set makes the template's "in" check fast
    taken_seat_ids = set(
        Booking.objects.filter(movie=movie).values_list('seat_id', flat=True)
    )

    # Group by row letter (first character of seat_number), e.g. {'A': [A1, A2, ...]}
    rows = {}
    for seat in seats:
        rows.setdefault(seat.seat_number[0], []).append(seat)
    # List of (row_letter, [seats]) tuples, rows in alphabetical order
    seat_rows = sorted(rows.items())

    return render(request, 'bookings/seat_booking.html', {
        'movie': movie,
        'seat_rows': seat_rows,
        'taken_seat_ids': taken_seat_ids
    })

# Shows only the logged-in user's bookings
@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})