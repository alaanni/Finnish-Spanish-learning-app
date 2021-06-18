from sqlalchemy.sql.operators import distinct_op
from db import db

def get_reviews(exercise_id):
    return