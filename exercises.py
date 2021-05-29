from db import db

def get_students_exercises(user_level):
    sql = "SELECT id, name FROM exercises WHERE level<=:user_level AND visible=1 ORDER BY level"
    return db.session.execute(sql, {"user_level":user_level}).fetchall()

def get_teachers_exercises(user_id):
    sql = "SELECT id, name FROM exercises WHERE creator_id=:user_id AND visible=1 ORDER BY level"
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
    sql = "SELECT id, name, level FROM exercises WHERE visible=1 ORDER BY name"
    return db.session.execute(sql).fetchall()

def get_info(exercise_id):
    sql = """SELECT e.name, e.level, u.username FROM exercises e, users u
             WHERE e.id=:exercise_id AND e.teacher_id=u.id"""
    return db.session.execute(sql, {"exercise_id": exercise_id}).fetchone()

def get_questions(exercise_id):
    return