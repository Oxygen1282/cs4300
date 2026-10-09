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
        read_only_fields = ["booking_date", 'user']    # auto-set by the model, clients can't send it, user is server-set

    def validate(self, data):
        # Reject a seat already booked for this movie (both API and web paths)
        movie = data.get('movie')
        seat = data.get('seat')
        if Booking.objects.filter(movie=movie, seat=seat).exists():
            raise serializers.ValidationError(
                "That seat is already bkkied for this movie."
            )
        return data 