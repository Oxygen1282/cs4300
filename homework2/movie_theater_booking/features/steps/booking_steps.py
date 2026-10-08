from behave import given, when, then 
from datetime import date 
from bookings.models import Movie, Seat

# Step definitions for features/movie_booking.feature.
# Run with: python manage.py behave  (behave-django uses a fresh test database)
# The "{title}"-style placeholders in each decorator are parsed out of the
# Gherkin step text and passed in as arguments.

@given('a movie "{title}" exists')
def step_create_movie(context, title):
    Movie.objects.create(
        title=title,
        description="Test description",
        release_date=date(2010, 7, 16),
        duration=148,
    )

@when('I visit the movie list page')
def step_visit_movie_list(context):
    # behave-django provides context.test.client - Django's test client
    context.response = context.test.client.get("/")

@then('I should see "{text}" in the response')
def step_check_response(context, text):
    assert text in context.response.content.decode(), \
        f'"{text}" not found in the page'


@given('a seat "{seat_number}" exists')
def step_create_seat(context, seat_number):
    context.seat = Seat.objects.create(seat_number=seat_number)


@then('the seat "{seat_number}" should not be booked')
def step_seat_not_booked(context, seat_number):
    from bookings.models import Booking 
    seat = Seat.objects.get(seat_number=seat_number)
    # "Not booked" means NO Booking references this seat (for any movie)
    assert not Booking.objects.filter(seat=seat).exists(), \
        f"Seat {seat_number} unexpectedly has a booking"