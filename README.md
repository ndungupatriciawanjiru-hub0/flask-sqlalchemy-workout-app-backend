# Workout Application Backend

A Flask REST API for tracking workouts and the exercises in them, built with Flask, SQLAlchemy, Flask-Migrate and Marshmallow. Personal trainers can create reusable exercises, log workouts, and attach exercises to workouts with sets, reps or duration.

## Models

- Exercise: id, name (unique), category, equipment_needed
- Workout: id, date, duration_minutes, notes
- WorkoutExercise (join table): id, workout_id, exercise_id, reps, sets, duration_seconds

A Workout has many Exercises through WorkoutExercises, and an Exercise has many Workouts through WorkoutExercises.

## Validations

- Table constraints: unique exercise name, non-blank exercise name, positive workout duration, non-negative reps/sets/duration_seconds
- Model validations: non-empty exercise name and category, positive workout duration, non-negative reps/sets/duration_seconds
- Schema validations: field length and range checks, a required valid date, reps requires sets, and reps or duration_seconds must be given

## Installation

Requires Python 3.8 or newer (developed with Python 3.12) and pipenv.

1. Clone the repo and cd into it.
2. Install dependencies and open the environment: `pipenv install`, then `pipenv shell`
3. Go to the server folder: `cd server`
4. Set up the database: `flask db init`, `flask db migrate -m "create tables"`, `flask db upgrade head`
5. Seed it: `python seed.py`

The migrations folder is already included in the repo. If you cloned it, skip `flask db init` and `flask db migrate`, and just run `flask db upgrade head` before seeding.

## Running

From the server directory run: `flask run -p 5555` (or `python app.py`). The API is at http://localhost:5555.

## Endpoints

- `GET /workouts`: list all workouts
- `GET /workouts/<id>`: one workout with its exercises, including reps, sets and duration
- `POST /workouts`: create a workout. JSON: date (YYYY-MM-DD), duration_minutes, notes (optional)
- `DELETE /workouts/<id>`: delete a workout and its workout exercises
- `GET /exercises`: list all exercises
- `GET /exercises/<id>`: one exercise with the workouts it appears in
- `POST /exercises`: create an exercise. JSON: name, category, equipment_needed (optional)
- `DELETE /exercises/<id>`: delete an exercise and its workout exercises
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`: add an exercise to a workout. JSON: reps and sets, or duration_seconds

Errors return JSON with an error or errors key: 400 for invalid data or constraint violations (such as a duplicate exercise name), and 404 when a record is not found.
