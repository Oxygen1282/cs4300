# Movie Theater Booking Application

A RESTful movie theater seat-booking application built with Python, Django, and
Django REST Framework. Users can browse movies, reserve seats from a visual seat
map, and view their booking history — through both a Bootstrap web interface and
a JSON API over the same data.

**Live site (Render):** https://movie-theater-booking-zlgm.onrender.com 

> Note: the live site runs on Render's free tier, which spins down after ~15
> minutes of inactivity. The first request after idle may take 30–60 seconds to
> wake the service.

---

## Features

- **Web UI (Django templates + Bootstrap 5)**
  - Movie listing page
  - Interactive seat map (A1–D8, 32 seats) with a "Screen" banner; click to
    select multiple seats, then confirm
  - Booking history page
- **REST API (Django REST Framework)**
  - Full CRUD for movies, seats, and bookings
- **Per-movie seat availability** — a seat taken for one movie is still
  available for other movies (availability is derived from the `Booking` table,
  not a global flag)
- **Authentication** — booking and history require login (unauthenticated users
  are redirected to the login page)

---

## Project Structure

```
movie_theater_booking/            # project root (contains manage.py)
├── manage.py
├── build.sh                      # Render build script (install, static, migrate, seed)
├── requirements.txt
├── runtime.txt                   # pins Python 3.12
├── movie_theater_booking/        # project configuration package
│   ├── settings.py               # env-aware settings (DEBUG, SECRET_KEY, hosts)
│   ├── urls.py                   # project URL routing
│   └── wsgi.py                   # WSGI entry point (used by Gunicorn)
├── bookings/                     # main application
│   ├── models.py                 # Movie, Seat, Booking
│   ├── serializers.py            # DRF serializers
│   ├── views.py                  # API ViewSets + template views
│   ├── urls.py                   # app URL routing (API router + page routes)
│   ├── admin.py                  # admin registrations
│   ├── tests.py                  # unit + integration tests
│   ├── templates/bookings/       # base, movie_list, seat_booking, booking_history
│   └── management/commands/
│       └── seed_data.py          # idempotent DB seeding (admin, seats, movies)
└── features/                     # Behave BDD tests
    ├── movie_booking.feature
    └── steps/booking_steps.py
```

---

## Data Model

- **Movie** — title, description, release date, duration (minutes)
- **Seat** — seat number (e.g. "A1")
- **Booking** — links a Movie, a Seat, and a User, with an auto-set booking date

A seat's availability is **not** stored on the seat. Instead, a seat is
considered booked *for a given movie* when a `Booking` row exists linking that
seat to that movie. This allows the same seat to be booked independently across
different movies.

---

## API Endpoints

| Endpoint          | Methods                 | Description                        |
|-------------------|-------------------------|------------------------------------|
| `/api/movies/`    | GET, POST, PUT, DELETE  | List/create/update/delete movies   |
| `/api/seats/`     | GET, POST, PUT, DELETE  | Seat records                        |
| `/api/bookings/`  | GET, POST, PUT, DELETE  | Bookings (create and view history)  |

The browsable DRF interface is available at these URLs in a web browser.

---

## Local Setup

1. **Activate the virtual environment and enter the project directory:**
```bash
   git clone https://github.com/Oxygen1282/cs4300.git
   cd cs4300/homework2/movie_theater_booking
   python -m venv venv
   source venv/bin/activate
```

2. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

3. **Create the `.env` file** (fill in your own secret key and admin password):
    (SKIP THIS IF YOU HAVE ALREADY CREATED .env)
```bash
   touch .env
   echo "DJANGO_SECRET_KEY=devloper_secret_key" >> .env
   echo "DJANGO_DEBUG=True" >> .env
   echo "DJANGO_ADMIN_PASSWORD=changeme" >> .env
```

4. **Apply migrations and seed the database:**
```bash
   python manage.py migrate
   python manage.py seed_data
```

5. **Run the server:**
```bash
   python manage.py runserver 0.0.0.0:3000
```
   Click the DevEdu app link, then log in at `/admin` with the admin account.

---

## Running the Tests

**Unit and integration tests:**
```bash
python manage.py test
```

**Test coverage:**
```bash
coverage run --source='.' manage.py test
coverage report
```

**Behavior-Driven (BDD) tests with Behave:**
```bash
python manage.py behave
```

---

## Deployment (Render)

The application is deployed as a Render Web Service connected to the GitHub repo.

- **Root Directory:** `homework2/movie_theater_booking`
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn movie_theater_booking.wsgi:application`
- **Environment variables (set in the Render dashboard):**
  - `DJANGO_SECRET_KEY`
  - `DJANGO_ADMIN_PASSWORD`
  - (`DJANGO_DEBUG` is left unset, so it defaults to `False` in production)

The build script runs `collectstatic`, `migrate`, and `seed_data` on each
deploy. Static files are served by WhiteNoise. The database is SQLite on an
ephemeral filesystem, so seeded data (admin, seats, movies) is rebuilt on every
deploy; user-created bookings do not persist across deploys.

---

## Use of AI Tools

**Tool used:** Anthropic Claude.

**What it was used for:**
- Explaining Django and Django REST Framework concepts (MVT architecture,
  serializers, viewsets, routing, migrations, templates, testing).
- Generating code for the models, serializers, views, URL configuration,
  templates (including the interactive seat map and its JavaScript), the
  `seed_data` management command, the test suite, the Behave tests, and the
  Render deployment configuration (`build.sh`, `requirements.txt`, settings
  changes).
- Debugging errors encountered during development (migration issues, URL
  routing, deployment build failures, and the per-movie seat-availability bug).
- Claude CLI tool was used to go through python and HTML files and add in-line
  dev comments. No code was changed or generated by the CLI tool.
- Claude generated the README with sections for the programmer to insert info 

**How the generated content was incorporated:**
- Code generated by the AI was typed out line by line to ensure that all decisions 
  ultimately made by the programmer. All design and logic decisions were reviewed and
  implemented/changed by the programmer. Most of the code is AI code, but the programmer
  has reviewed, understood, and accepted this code. All code was generated from a Claude
  prompt, and No code (only comments) has been produced by the Claude CLI tool.