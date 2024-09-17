from flask import Flask, render_template, redirect, url_for
from cache import Globals

app = Flask(__name__)


def i18n_get(lang: str = "en_us"):
    return Globals.i18n_cache.get_or_create(lang).get


@app.route("/")
def index():
    return render_template("index.html", i18n=i18n_get())


@app.route("/login")
def login():
    return render_template("login/login.html", i18n=i18n_get())


@app.route("/login/student", methods=["GET, POST"])
def login_student():
    return render_template("login/student.html", i18n=i18n_get())


@app.route("/login/teacher", methods=["GET", "POST"])
def login_teacher():
    return render_template("login/teacher.html", i18n=i18n_get())


@app.route("/login/personal", methods=["GET", "POST"])
def login_personal():
    return render_template("login/personal.html", i18n=i18n_get())


@app.route("/register")
def register():
    return redirect(url_for("login"))


@app.route("/register/personal", methods=["GET", "POST"])
def register_personal():
    return render_template("register/personal.html", i18n=i18n_get())


@app.route("/register/teacher", methods=["GET", "POST"])
def register_teacher():
    return render_template("register/teacher.html", i18n=i18n_get())


if __name__ == '__main__':
    app.run()
