from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(load_default=False)

    workout_exercises = fields.Nested(
        'WorkoutExerciseSchema', many=True, dump_only=True,
        only=('id', 'workout', 'reps', 'sets', 'duration_seconds'))

    @validates_schema
    def validate_not_blank(self, data, **kwargs):
        for field in ('name', 'category'):
            if field in data and not data[field].strip():
                raise ValidationError('Must not be blank.', field)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=1), allow_none=True)
    sets = fields.Int(validate=validate.Range(min=1), allow_none=True)
    duration_seconds = fields.Int(validate=validate.Range(min=1), allow_none=True)

    exercise = fields.Nested(ExerciseSchema, dump_only=True,
                             only=('id', 'name', 'category', 'equipment_needed'))
    workout = fields.Nested('WorkoutSchema', dump_only=True,
                            only=('id', 'date', 'duration_minutes'))

    @validates_schema
    def validate_effort(self, data, **kwargs):
        """A workout exercise needs reps (with sets) or a duration."""
        has_reps = data.get('reps') is not None
        has_duration = data.get('duration_seconds') is not None
        if not has_reps and not has_duration:
            raise ValidationError('Provide reps (and sets) or duration_seconds.')
        if has_reps and data.get('sets') is None:
            raise ValidationError('sets is required when reps is given.', 'sets')


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True, validate=validate.Length(max=1000))

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema, many=True, dump_only=True,
        only=('id', 'exercise', 'reps', 'sets', 'duration_seconds'))


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=('workout_exercises',))
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=('workout_exercises',))
workout_exercise_schema = WorkoutExerciseSchema()