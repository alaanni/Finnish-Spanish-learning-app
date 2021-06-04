from sqlalchemy.sql.operators import distinct_op
from db import db

def get_teachers_exercises(user_id):
    sql = "SELECT id, name FROM exercises WHERE teacher_id=:user_id AND visible=1 ORDER BY name"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def add_exercise(name, level, words, teacher_id):
    sql = """INSERT INTO exercises (teacher_id, name, level, visible)
             VALUES (:teacher_id, :name, :level, 1) RETURNING id"""
    exercise_id = db.session.execute(sql, {"teacher_id":teacher_id, "name":name, "level":level}).fetchone()[0]

    for pair in words.split("\n"):
        parts = pair.strip().split(";")
        if len(parts) != 2:
            continue

        sql = """INSERT INTO questions (exercise_id, fin, spa)
                 VALUES (:exercise_id, :fin, :spa)"""
        db.session.execute(sql, {"exercise_id":exercise_id, "fin":parts[0], "spa":parts[1]})

    db.session.commit()
    return exercise_id

def get_all_exercises():
    sql = "SELECT id, name, level FROM exercises WHERE visible=1 ORDER BY level"
    return db.session.execute(sql).fetchall()

def get_info(exercise_id):
    sql = """SELECT e.name, e.level, u.username FROM exercises e, users u
             WHERE e.id=:exercise_id AND e.teacher_id=u.id"""
    return db.session.execute(sql, {"exercise_id": exercise_id}).fetchone()

def get_questions(exercise_id):
    sql = "SELECT id, exercise_id, fin, spa FROM questions WHERE exercise_id=:exercise_id"
    return db.session.execute(sql, {"exercise_id":exercise_id}).fetchall()

def get_level(exercise_id):
    sql = "SELECT level FROM exercises WHERE id=:exercise_id"
    return db.session.execute(sql, {"exercise_id": exercise_id}).fetchone()

def check_answer(question_id, answer, user_id, level):
    sql = "SELECT fin, spa FROM questions WHERE id=:id"
    correct = db.session.execute(sql, {"id":question_id}).fetchone()
    if level < 2:
        result = 1 if answer == correct[1] else 0
    else:
        result = 1 if answer == correct[0] else 0
    if result == 1:
        sql = "UPDATE users SET points=points+1 WHERE id=:user_id"
        db.session.execute(sql, {"user_id":user_id})
        db.session.commit()
    sql = """INSERT INTO answers (question_id, user_id, result)
             VALUES (:question_id, :user_id, :result)"""
    db.session.execute(sql, {"question_id":question_id, "user_id":user_id, "result":result})
    db.session.commit()

def count_questions(exercise_id):
    sql = "SELECT COUNT(*) FROM questions WHERE exercise_id=:exercise_id"
    return db.session.execute(sql, {"exercise_id":exercise_id}).fetchone()[0]

def count_correct_answers(exercise_id, user_id):
    sql = """SELECT COUNT(DISTINCT question_id) FROM answers 
    JOIN questions ON answers.question_id = questions.id
    WHERE questions.exercise_id=:exercise_id AND result = 1 AND user_id=:user_id"""
    return db.session.execute(sql, {"exercise_id":exercise_id, "user_id":user_id}).fetchone()[0]

def remove_exercise(exercise_id, teacher_id):
    sql = """UPDATE exercises SET visible=0 
    WHERE id=:exercise_id and teacher_id=:teacher_id"""
    db.session.execute(sql, {"exercise_id":exercise_id, "teacher_id":teacher_id})
    db.session.commit()