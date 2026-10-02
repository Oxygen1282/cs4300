from django.contrib import admin
from .models import Movie, Seat, Booking

# Register your models here.
admin.site.register(Movie)
admin.site.register(Seat)
admin.site.register(Booking)

# Dev env Admin Login:
# username: david
# password: DjangoHw2Password