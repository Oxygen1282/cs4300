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
        # On a partial update the fields may be absent; fall back to the instance's values
        movie = data.get('movie') or getattr(self.instance, 'movie', None)
        seat = data.get('seat') or getattr(self.instance, 'seat', None)

        duplicates = Booking.objects.filter(movie=movie, seat=seat)
        if self.instance is not None:
            duplicates = duplicates.exclude(pk=self.instance.pk)    # ignore myself

        if duplicates.exists():
            raise serializers.ValidationError(
                "That seat is already booked for this movie."
            )
        return data