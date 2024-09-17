from flask import Flask, render_template
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


@app.route("/login/student")
def login_student():
    return render_template("login/student.html", i18n=i18n_get())


@app.route("/login/teacher")
def login_teacher():
    return render_template("login/teacher.html", i18n=i18n_get())


@app.route("/login/personal")
def login_personal():
    return render_template("base.html", i18n=i18n_get())


if __name__ == '__main__':
    app.run()
