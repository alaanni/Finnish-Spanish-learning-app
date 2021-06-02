import random
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

    return render_template("exercise.html", id=id, name=info[0], level=info[1], teacher=info[2])

@app.route("/study/<int:id>", methods=["get", "post"])
def study(id):
    questions = exercises.get_questions(id)
    choices = []
    for question in questions:
        choices.append(question[3])
    random.shuffle(choices)
    exercise_level = exercises.get_level(id)

    if request.method == "GET":
        return render_template("study.html", questions=questions, level=exercise_level, choices=choices)

    if request.method == "POST":
        users.require_role(1)
        users.check_csrf()

        exercise_id = request.form["exercise_id"]
        question_id = request.form["question_id"]
        answer = request.form["answer"]

        if exercises.check_answer(question_id, answer, exercise_id) == 1:
            for question in questions:
                if question[0] == question_id:
                    questions.remove(question)

        return render_template("study.html", questions=questions, level=exercise_level, choices=choices)