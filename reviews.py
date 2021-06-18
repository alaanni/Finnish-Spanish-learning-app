from db import db

def get_full_reviews(user_id):
    sql = """SELECT name, rating, feedback FROM reviews 
    JOIN exercises ON reviews.exercise_id = exercises.id
    WHERE exercises.teacher_id =:user_id"""
    return db.session.execute(sql, {"user_id": user_id}).fetchall()

def get_reviews_average(exercise_id):
    sql = "SELECT rating FROM reviews WHERE exercise_id=:exercise_id"
    return db.session.execute(sql, {"exercise_id": exercise_id}).fetchall()

def add_review(exercise_id, user_id, rating, feedback):
    sql = """INSERT INTO reviews (exercise_id, user_id, rating, feedback)
             VALUES (:exercise_id, :user_id, :rating, :feedback)"""
    db.session.execute(sql, {"exercise_id":exercise_id, "user_id":user_id, "rating":rating, "feedback":feedback})
    db.session.commit()