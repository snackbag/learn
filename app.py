from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import func

import helper
import database as db
from cache import Globals

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"


def i18n_get(lang: str = "en_us"):
    return Globals.i18n_cache.get_or_create(lang).get


@app.route("/")
def index():
    return render_template("index.html", i18n=i18n_get())


@app.route("/login")
def login():
    return render_template("login/login.html", i18n=i18n_get())


@app.route("/login/student", methods=["GET", "POST"])
def login_student():
    if request.method == "POST":
        if not helper.has_keys(["classcode", "username", "password"], request.form):
            return "Illegal request: Request form requires classcode, username and password"

        classcode = request.form["classcode"]
        username = request.form["username"]
        password = request.form["password"]

        if len(classcode) != 8:
            return "Classcode must be 8 characters long"

        if len(username) < 2 or len(username) > 20:
            return "Username must be between 2 and 20 characters long"

        if len(password) < 4 or len(password) > 30:
            return "Password must be between 4 and 30 characters long"

        i18n = i18n_get()

        query = db.session.query(db.ClassCode).filter_by(key=classcode).first()

        if query is None:
            flash(i18n("error.notfound.class"))

    return render_template("login/student.html", i18n=i18n_get())


@app.route("/login/teacher", methods=["GET", "POST"])
def login_teacher():
    return render_template("login/teacher.html", i18n=i18n_get())


@app.route("/login/personal", methods=["GET", "POST"])
def login_personal():
    if request.method == "POST":
        if not helper.has_keys(["email", "password"], request.form):
            return "Illegal request: Request form requires email and password"

        email = request.form["email"]
        password = request.form["password"]

        if len(email) < 8 or len(email) > 50:
            return "Email must be between 8 and 50 characters long"

        if len(password) < 8 or len(password) > 50:
            return "Password must be between 8 and 50 characters long"

        i18n = i18n_get()
        email_query = db.session.query(db.User).filter(
            func.lower(db.User.email) == func.lower(email),
            db.User.account_type != 2
        ).first()

        if email_query is None:
            flash(i18n("error.notfound.user"))
            return render_template("login/personal.html", i18n=i18n)

        if not helper.verify_password(email_query.salt, email_query.password, password):
            flash(i18n("error.notfound.user"))
            return render_template("login/personal.html", i18n=i18n)

        flash("OK")

    return render_template("login/personal.html", i18n=i18n_get())


@app.route("/register")
def register():
    return redirect(url_for("login"))


@app.route("/register/personal", methods=["GET", "POST"])
def register_personal():
    if request.method == "POST":
        if not helper.has_keys(["email", "username", "password"], request.form):
            return "Illegal request: Request form requires email, username and password"

        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        if len(email) < 8 or len(email) > 50:
            return "Email must be between 8 and 50 characters long"

        if len(username) < 4 or len(username) > 26:
            return "Username must be between 4 and 26 characters long"

        if len(password) < 8 or len(password) > 50:
            return "Password must be between 8 and 50 characters long"

        i18n = i18n_get()

        email_query = db.session.query(db.User).filter(
            func.lower(db.User.email) == func.lower(email),
            db.User.account_type != 2
        ).first()

        if email_query is not None:
            flash(i18n("error.exists.email"))

        username_query = db.session.query(db.User).filter(
            func.lower(db.User.username) == func.lower(username),
            db.User.account_type != 2
        ).first()

        if username_query is not None:
            flash(i18n("error.exists.username"))

        if username_query is not None or email_query is not None:
            return render_template("register/personal.html", i18n=i18n)

        pwd = helper.create_password(password)

        db.session.add(db.User(
            account_type=0,
            email=email,
            username=username,
            salt=pwd[0],
            password=pwd[1]
        ))
        db.session.commit()

    return render_template("register/personal.html", i18n=i18n_get())


@app.route("/register/teacher", methods=["GET", "POST"])
def register_teacher():
    return render_template("register/teacher.html", i18n=i18n_get())


if __name__ == '__main__':
    app.run()
