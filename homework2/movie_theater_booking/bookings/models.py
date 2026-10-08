from django.db import models
from django.contrib.auth.models import User 

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="length in minutes")

    def __str__(self):
        return self.title 

# A physical seat, shared by every movie. Whether it's taken is tracked per
# movie through Booking, not stored on the Seat itself.
class Seat(models.Model):
    # e.g. "A1", "B12"; the first character is used as the row letter in views.seat_booking
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return self.seat_number

# One user holding one seat for one movie. A seat is "taken" for a movie
# when a Booking with that (movie, seat) pair exists.
class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)     # set once, when the booking is created

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.seat.seat_number}"