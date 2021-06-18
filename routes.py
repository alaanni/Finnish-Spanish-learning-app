import random

from flask.globals import session
from app import app
from flask import redirect, render_template, request
from flask import render_template
import users, exercises

@app.route("/")
def index():
    return render_template("index.html", exercises=exercises.get_all_exercises())

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password1"]
        password2 = request.form["password2"]
        role = request.form["role"]
        if len(username) < 1 or len(username) > 15:
            return render_template("error.html", message="Käyttäjätunnuksessa tulee olla 1-15 merkkiä")
        if password != password2:
            return render_template("error.html", "salasanat eivät täsmää")
        if password == "":
            return render_template("error.html", message="Anna käyttäjälle salasana")
        if role != "1" and role != "2":
            return render_template("error.html", message="Tuntematon käyttäjärooli")

        if users.register(username, password, role):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/add", methods=["get", "post"])
def add_exercise():
    users.require_role(2)

    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        if len(name) < 1 or len(name) > 15:
            return render_template("error.html", message="Nimessä tulee olla 1-15 merkkiä")

        level = request.form["level"]
        if level != "0" and level != "1" and level != "2" and level != "3":
            return render_template("error.html", message="Tuntematon taitotaso")

        words = request.form["words"]
        if len(words) > 500:
            return render_template("error.html", message="Sanalista on liian pitkä")

        exercise_id = exercises.add_exercise(name, level, words, users.user_id())
        return redirect("/exercise/"+str(exercise_id))

@app.route("/exercise/<int:id>")
def exercise(id):
    info = exercises.get_info(id)
    questions = exercises.count_questions(id)
    correct_answers = exercises.count_correct_answers(id, users.user_id())
    users.check_points()
    users.check_level()

    return render_template("exercise.html", id=id, name=info[0], level=info[1], teacher=info[2], 
    questions=questions, answers=correct_answers)

@app.route("/study/<int:id>", methods=["get", "post"])
def study(id):
    questions = exercises.get_questions(id)
    choices = []
    for question in questions:
        choices.append(question[3])
    random.shuffle(choices)
    exercise_level = exercises.get_level(id)[0]

    if request.method == "GET":
        return render_template("study.html", questions=questions, level=exercise_level, choices=choices)

    if request.method == "POST":
        users.require_role(1)
        users.check_csrf()

        question_id = request.form["question_id"]
        answer = request.form["answer"]

        exercises.check_answer(question_id, answer, users.user_id(), exercise_level)

        return render_template("study.html", questions=questions, level=exercise_level, choices=choices)

@app.route("/remove", methods=["get", "post"])
def remove_exercise():
    users.require_role(2)

    if request.method == "GET":
        list = exercises.get_teachers_exercises(users.user_id())
        return render_template("remove.html", exercises=list)

    if request.method == "POST":
        users.check_csrf()
        if "exercise" in request.form:
            exercise = request.form["exercise"]
            exercises.remove_exercise(exercise, users.user_id())
        

        return redirect("/remove")

@app.route("/stats")
def stats():
    users.require_role(2)
    list = exercises.get_teachers_exercises(users.user_id())
    statistics = exercises.get_stats(users.user_id())

    return render_template("stats.html", exercises=list, statistics=statistics)

@app.route("/review/<int:id>", methods=["get", "post"])
def review(id):
    if request.method == "GET":
        return render_template("review.html", id=id)

    if request.method == "POST":
        users.require_role(1)
        users.check_csrf()

        return render_template("review.html", id=id)