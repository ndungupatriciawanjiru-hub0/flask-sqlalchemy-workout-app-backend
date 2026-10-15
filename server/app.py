from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (exercise_schema, exercises_schema, workout_schema,
                     workouts_schema, workout_exercise_schema)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


def error(message, status):
    return jsonify({'error': message}), status


def save(obj):
    """Add and commit; convert DB/model errors into a 400 response."""
    try:
        db.session.add(obj)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return str(e.orig) if isinstance(e, IntegrityError) else str(e)
    return None


# ---------- Workouts ----------
@app.get('/workouts')
def get_workouts():
    return jsonify(workouts_schema.dump(Workout.query.all())), 200


@app.get('/workouts/<int:id>')
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error('Workout not found', 404)
    return jsonify(workout_schema.dump(workout)), 200


@app.post('/workouts')
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    try:
        workout = Workout(**data)
    except ValueError as e:
        return error(str(e), 400)
    err = save(workout)
    if err:
        return error(err, 400)
    return jsonify(workout_schema.dump(workout)), 201


@app.delete('/workouts/<int:id>')
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error('Workout not found', 404)
    # cascade removes associated WorkoutExercises
    db.session.delete(workout)
    db.session.commit()
    return '', 204


# ---------- Exercises ----------
@app.get('/exercises')
def get_exercises():
    return jsonify(exercises_schema.dump(Exercise.query.all())), 200


@app.get('/exercises/<int:id>')
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error('Exercise not found', 404)
    return jsonify(exercise_schema.dump(exercise)), 200


@app.post('/exercises')
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    try:
        exercise = Exercise(**data)
    except ValueError as e:
        return error(str(e), 400)
    err = save(exercise)
    if err:
        return error(err, 400)
    return jsonify(exercise_schema.dump(exercise)), 201


@app.delete('/exercises/<int:id>')
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error('Exercise not found', 404)
    db.session.delete(exercise)
    db.session.commit()
    return '', 204


# ---------- Add exercise to workout ----------
@app.post('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises')
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout:
        return error('Workout not found', 404)
    if not exercise:
        return error('Exercise not found', 404)
    try:
        data = workout_exercise_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    try:
        we = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
    except ValueError as e:
        return error(str(e), 400)
    err = save(we)
    if err:
        return error(err, 400)
    return jsonify(workout_exercise_schema.dump(we)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)