from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from datetime import date
from .models import Movie, Seat, Booking 

# Create your tests here.

# -------------- UNIT TESTS: Models in isolation -----------------
class MovieModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Inception",
            description="A thief who steals corporate secrets.",
            release_date=date(2010, 7, 16),
            duration=148,
        )
    
    def test_movie_str(self):
        # __str__ should return the title
        self.assertEqual(str(self.movie), "Inception")

    def test_movie_fields(self):
        self.assertEqual(self.movie.duration, 148)
        self.assertEqual(self.movie.title, "Inception")

class SeatModelTest(TestCase):
    def test_seat_str(self):
        seat = Seat.objects.create(seat_number="A1")
        self.assertEqual(str(seat), "A1")

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dave", password="pw12345")
        self.movie = Movie.objects.create(
            title="Dune",
            description="Desert planet.",
            release_date=date(2021, 10, 22),
            duration=155,
        )
        self.seat = Seat.objects.create(seat_number="B3")

    def test_booking_creation(self):
        booking = Booking.objects.create(
            movie=self.movie, seat=self.seat, user=self.user
        )
        self.assertEqual(booking.movie.title, "Dune")
        self.assertEqual(booking.seat.seat_number, "B3")
        # booking_date is auto-set on creation, so it must not be empty
        self.assertIsNotNone(booking.booking_date)


# ---------- INTEGRATION TESTS: API endpoints end-to-end ----------
class MovieAPITest(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Arrival",
            description="Linguist meets aliens.",
            release_date=date(2016, 11, 11),
            duration=116,
        )

    def test_list_movies(self):
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_movie(self):
        payload = {
            "title": "Interstellar",
            "description": "Space and time.",
            "release_date": "2014-11-07",
            "duration": 169,
        }
        response = self.client.post("/api/movies/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)

class BookingAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dave", password="pw12345")
        self.movie = Movie.objects.create(
            title="Tenet",
            description="Time inversion.",
            release_date=date(2020, 8, 26),
            duration=150,
        )
        self.seat = Seat.objects.create(seat_number="C5")

    def test_create_booking_via_api(self):
        self.client.force_authenticate(user=self.user)      # log in for the request
        payload = {
            "movie": self.movie.id,
            "seat": self.seat.id,
            "user": self.user.id,
        }
        response = self.client.post("/api/bookings/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

class SeatBookingViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dave", password = "pw12345")
        self.movie = Movie.objects.create(
            title="Heat", 
            description="Cops and robbers.",
            release_date=date(1995, 12, 15), 
            duration=170,
        )
        self.seat_a1 = Seat.objects.create(seat_number="A1")
        self.seat_a2 = Seat.objects.create(seat_number="A2")
        # log the test client in, since seat_booking needs request.user
        self.client.login(username="dave", password="pw12345")

    def test_seat_booking_page_loads(self):
        # GET should render the seat map with a 200
        response = self.client.get(f"/book/{self.movie.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("seat_rows", response.context)

    def test_booking_multiple_seats(self):
        # POST a list of seat ids; both should be booked
        response = self.client.post(
            f"/book/{self.movie.id}/",
            {"seats": [self.seat_a1.id, self.seat_a2.id]}
        )
        # successful booking redirects to history
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 2)
        # Availability lives in Booking not the seat
        self.assertTrue(Booking.objects.filter(movie=self.movie, seat=self.seat_a1).exists())
        self.assertTrue(Booking.objects.filter(movie=self.movie, seat=self.seat_a2).exists())

    def test_booking_skips_already_booked_seat(self):
        # pre-book A1, then try to book both A1 and A2
        Booking.objects.create(movie=self.movie, seat=self.seat_a1, user=self.user)
        response = self.client.post(
            f"/book/{self.movie.id}/",
            {"seats": [self.seat_a1.id, self.seat_a2.id]},
        )
        self.assertEqual(response.status_code, 302)
        # only A2 should have been booked; A1 was skipped
        self.assertEqual(Booking.objects.count(), 2)
        self.assertEqual(Booking.objects.filter(seat=self.seat_a2).count(), 1)

    def test_booking_for_other_movie(self):
        # Book A1 for movie 1; A1 should still be free for a DIFFERENT movie
        other_movie = Movie.objects.create(
            title="Other", description="x", release_date=date(2020, 1, 1), duration=100,
        )
        Booking.objects.create(movie=self.movie, seat=self.seat_a1, user=self.user)
        response = self.client.get(f"/book/{other_movie.id}/")
        self.assertNotIn(self.seat_a1.id, response.context['taken_seat_ids'])

class TemplateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dave", password="pw12345")
        self.movie = Movie.objects.create(
            title="Up",
            description="Balloons.",
            release_date=date(2009, 5, 29), 
            duration=96,
        )
        self.client.login(username="dave", password="pw12345")

    def test_movie_list_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Up")     # The movie title appears in the HTML

    def test_booking_history_page(self):
        response = self.client.get("/bookings/history/")
        self.assertEqual(response.status_code, 200)