from rest_framework import serializers
from .models import Movie, Seat, Booking

# ModelSerializers convert model instances to/from JSON for the API.
# fields = "__all__" exposes every model field; foreign keys appear as ids.

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat 
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking 
        fields = "__all__"
        read_only_fields = ["booking_date"]    # auto-set by the model, clients can't send it