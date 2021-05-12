from app import app
from flask import redirect, render_template, request
from flask import render_template
import users

@app.route("/")
def index():
    return render_template("index.html")

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