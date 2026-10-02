import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User 
from datetime import date 
from bookings.models import Movie, Seat 

class Command(BaseCommand):
    help = "Seed the database with an admin user, seats, and movies (idempotent)."

    def handle(self, *args, **options):
        self.create_admin()
        self.create_seats()
        self.create_movies()
        self.stdout.write(self.style.SUCCESS("Seeding complete."))

    def create_admin(self):
        username = os.environ.get('DJANGO_ADMIN_USER', 'admin')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD')
        if not password:
            self.stdout.write("No DJANGO_ADMIN_PASSWORD set - skipping admin creation.")
            return 
        # get_or_create avoids a duplicate-username crash on re-run
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'is_staff': True, 'is_superuser': True},
        )
        if created:
            user.set_password(password)     # hash the password properly
            user.save()
            self.stdout.write(f"Created superuser '{username}'.")
        else:
            self.stdout.write(f"Superuser '{username}' already exists - skipping.")
    
    def create_seats(self):
        rows = ['A', 'B', 'C', 'D']
        created_count = 0
        for row in rows:
            for num in range(1, 9):     # 1 - 8
                seat_number = f"{row}{num}"
                # get_or_create: only makes it if missing
                _, created = Seat.objects.get_or_create(seat_number=seat_number)
                if created:
                    created_count += 1
        self.stdout.write(f"Seats: created {created_count}, total now {Seat.objects.count()}.")

    def create_movies(self):
        movies = [
            {"title": "Inception", "description": "A thief who steals corporate secrets through dreams.",
             "release_date": date(2010, 7, 16), "duration": 148},
            {"title": "Dune", "description": "A young noble's rise on a desert planet.",
             "release_date": date(2021, 10, 22), "duration": 155},
            {"title": "Arrival", "description": "A linguist makes contact with alien visitors.",
             "release_date": date(2016, 11, 11), "duration": 116},
            {"title": "Interstellar", "description": "Explorers travel through a wormhole in space.",
             "release_date": date(2014, 11, 7), "duration": 169},
            {"title": "The Matrix", "description": "A hacker discovers reality is a simulation.",
             "release_date": date(1999, 3, 31), "duration": 136},
        ]
        created_count = 0
        for m in movies:
            # match on title so re-runs don't duplicate
            _, created = Movie.objects.get_or_create(title=m["title"], defaults=m)
            if created: 
                created_count += 1
        self.stdout.write(f"Movies: created {created_count}, total now {Movie.objects.count()}.")