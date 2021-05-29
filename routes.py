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
            return render_template("error.html",message="Väärä tunnus tai salasana")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password1"]
        password2 = request.form["password2"]
        role = request.form["role"]
        level = 0
        if len(username) < 1 or len(username) > 15:
            return render_template("error.html", message="Käyttäjätunnuksessa tulee olla 1-15 merkkiä")
        if password != password2:
            return render_template("error.html", "salasanat eivät täsmää")
        if password == "":
            return render_template("error.html", message="Anna käyttäjälle salasana")
        if role != "1" and role != "2":
            return render_template("error.html", message="Tuntematon käyttäjärooli")

        if users.register(username, password, role, level):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/add", methods=["get", "post"])
def add_deck():
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
def deck(id):
    info = exercises.get_info(id)

    return render_template("exercise.html", id=id, name=info[0], level=info[1], teacher=info[2])