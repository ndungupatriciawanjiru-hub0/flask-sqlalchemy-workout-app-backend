from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    # Table constraints: name can't be blank
    __table_args__ = (
        db.CheckConstraint('length(name) > 0', name='ck_exercise_name_not_empty'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = association_proxy('workout_exercises', 'workout')

    # Model validations
    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError('Exercise name cannot be empty.')
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        if not value or not value.strip():
            raise ValueError('Exercise category cannot be empty.')
        return value.strip()

    def __repr__(self):
        return f'<Exercise {self.id} {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    # Table constraint: duration must be positive
    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='ck_workout_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # Relationships
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises = association_proxy('workout_exercises', 'exercise')

    # Model validation
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError('duration_minutes must be a positive integer.')
        return value

    def __repr__(self):
        return f'<Workout {self.id} {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    # Table constraints: no negative values
    __table_args__ = (
        db.CheckConstraint('reps IS NULL OR reps >= 0', name='ck_we_reps_nonneg'),
        db.CheckConstraint('sets IS NULL OR sets >= 0', name='ck_we_sets_nonneg'),
        db.CheckConstraint('duration_seconds IS NULL OR duration_seconds >= 0',
                           name='ck_we_duration_nonneg'),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # Model validation: reps/sets/duration must be non-negative integers
    @validates('reps', 'sets', 'duration_seconds')
    def validate_non_negative(self, key, value):
        if value is not None and (not isinstance(value, int) or value < 0):
            raise ValueError(f'{key} must be a non-negative integer.')
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}>'