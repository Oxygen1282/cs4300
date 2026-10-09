from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from datetime import date
from .models import Movie, Seat, Booking

# Run with: python manage.py test bookings
# Each test gets a fresh, empty test database, so setUp builds what it needs.

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
        self.user = User.objects.create_user(username="dave", password="pw12345")
        self.movie = Movie.objects.create(
            title="Arrival",
            description="Linguist meets aliens.",
            release_date=date(2016, 11, 11),
            duration=116,
        )

    def test_list_movies(self):
        # Only the one movie from setUp should come back (no pagination configured)
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_movie(self):
        self.client.force_authenticate(user=self.user)      # writes now need auth
        payload = {
            "title": "Interstellar",
            "description": "Space and time.",
            "release_date": "2014-11-07",
            "duration": 169,
        }
        response = self.client.post("/api/movies/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)     # the setUp movie + the new one

    def test_anonymous_cannot_create_movie(self):
        payload = {
            "title": "X",
            "description": "x",
            "release_data": "2020-01-01",
            "duration": 100
        }
        response = self.client.post("/api/movies/", payload)    # no auth
        self.assertIn(response.status_code, [401, 403])

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
        # Log in for the request. It mirrors a real user booking.
        self.client.force_authenticate(user=self.user)
        payload = {
            "movie": self.movie.id,
            "seat": self.seat.id,       # user is sever-set
        }
        response = self.client.post("/api/bookings/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_api_rejects_duplicate_booking(self):
        # Booking the same seat for the same movie twice should fail the 2nd time
        self.client.force_authenticate(user=self.user)
        payload = {
            "movie": self.movie.id,
            "seat": self.seat.id,
        }
        first = self.client.post("/api/bookings/", payload)
        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        second = self.client.post("/api/bookings/", payload)
        self.assertEqual(second.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 1)    # no duplicate created
    
    def test_api_requires_authentication(self):
        # Anonymous POST should be rejected now that IsAuthenticated is set
        payload = {
            "movie": self.movie.id,
            "seat": self.seat.id,
        }
        response = self.client.post("/api/bookings/", payload)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Booking.objects.count(), 0)

    def test_api_forces_logged_in_user(self):
        # Even if a client sends a different user id, the booking is owned by
        # the authenticated user (user is read-only / server-set)
        other = User.objects.create_user(username="someone_else", password="pw")
        self.client.force_authenticate(user=self.user)
        payload = {
            "movie": self.movie.id,
            "seat": self.seat.id,
            "user": other.id,
        }
        response = self.client.post("/api/bookings/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.get()
        self.assertEqual(booking.user, self.user)   # NOT 'other'

    def test_seat_availability_endpoint(self):
        self.client.force_authenticate(user=self.user)
        # book the setUp seat for the movie
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        response = self.client.get(f"/api/seats/availability/?movie={self.movie.id}")
        self.assertEqual(response.status_code, 200)
        # find the booked seat in the response and confirm it reads as unavailable
        booked = next(s for s in response.data if s["id"] == self.seat.id)
        self.assertFalse(booked["is_available"])

    def test_seat_availability_requires_movie(self):
        response = self.client.get("/api/seats/availability/")
        self.assertEqual(response.status_code, 400)

    def test_user_sees_only_own_bookings(self):
        other = User.objects.create_user(username="other", password="pw")
        Booking.objects.create(movie=self.movie, seat=self.seat, user=other)
        self.client.force_authenticate(user=self.user)      # self.user has none
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)     # can't see other's bookings

    def test_user_cannot_delete_others_booking(self):
        other = User.objects.create_user(username="other", password="pw")
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=other)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/booking/{booking.id}/")
        self.assertEqual(response.status_code, 404)     # not in their queryset
        self.assertTrue(Booking.objects.filter(id=booking.id).exists())     # still there

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
        # log the test client in, since seat_booking is @login_required and uses request.user
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
        # only A2 should have been booked; A1 was skipped.
        # Count is 2 = the pre-existing A1 booking + the new A2 booking
        self.assertEqual(Booking.objects.count(), 2)
        self.assertEqual(Booking.objects.filter(seat=self.seat_a2).count(), 1)

    def test_booking_for_other_movie(self):
        # Book A1 for self.movie; A1 should still be free for a DIFFERENT movie
        # (regression test for the "seat taken for unrelated movies" bug)
        other_movie = Movie.objects.create(
            title="Other", description="x", release_date=date(2020, 1, 1), duration=100,
        )
        Booking.objects.create(movie=self.movie, seat=self.seat_a1, user=self.user)
        response = self.client.get(f"/book/{other_movie.id}/")
        self.assertNotIn(self.seat_a1.id, response.context['taken_seat_ids'])

# Smoke tests: the HTML pages render with a 200
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