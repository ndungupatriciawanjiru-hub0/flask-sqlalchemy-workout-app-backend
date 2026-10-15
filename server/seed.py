#!/usr/bin/env python3
from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print('Clearing tables...')
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print('Creating exercises...')
    exercises = [
        Exercise(name='Push-ups', category='Strength', equipment_needed=False),
        Exercise(name='Squats', category='Strength', equipment_needed=False),
        Exercise(name='Deadlift', category='Strength', equipment_needed=True),
        Exercise(name='Plank', category='Core', equipment_needed=False),
        Exercise(name='Jump Rope', category='Cardio', equipment_needed=True),
    ]
    db.session.add_all(exercises)
    db.session.commit()
    pushups, squats, deadlift, plank, rope = exercises

    print('Creating workouts...')
    workouts = [
        Workout(date=date(2026, 10, 5), duration_minutes=45, notes='Full body strength'),
        Workout(date=date(2026, 10, 7), duration_minutes=30, notes='Core and cardio'),
        Workout(date=date(2026, 10, 9), duration_minutes=60, notes='Heavy lift day'),
    ]
    db.session.add_all(workouts)
    db.session.commit()
    w1, w2, w3 = workouts

    print('Linking exercises to workouts...')
    db.session.add_all([
        WorkoutExercise(workout=w1, exercise=pushups, reps=15, sets=3),
        WorkoutExercise(workout=w1, exercise=squats, reps=12, sets=4),
        WorkoutExercise(workout=w2, exercise=plank, duration_seconds=60),
        WorkoutExercise(workout=w2, exercise=rope, duration_seconds=300),
        WorkoutExercise(workout=w3, exercise=deadlift, reps=5, sets=5),
        WorkoutExercise(workout=w3, exercise=squats, reps=8, sets=4),
    ])
    db.session.commit()
    print('Done seeding.')