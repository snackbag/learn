import functools
from pathlib import Path

from flask import Flask, render_template, redirect, url_for, request, flash, session, g, send_file
from sqlalchemy import func

import database as db
import helper
from cache import Globals

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"


def i18n_get(lang: str = "en_us"):
    return Globals.i18n_cache.get_or_create(lang).get


@app.before_request
def load_logged_in_user():
    user_id = str(session.get('user_id'))
    if not Globals.user_id_cache.should_use(user_id):
        g.user = None
    else:
        g.user = user_id
        g.user_db = db.session.query(db.User).filter_by(user_id=int(user_id)).first()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login"))
        return view(**kwargs)
    return wrapped_view


def not_logged_in(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            return redirect(url_for("panel"))
        return view(**kwargs)
    return wrapped_view


@app.route("/")
@not_logged_in
def index():
    return render_template("index.html", i18n=i18n_get())


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/login")
@not_logged_in
def login():
    return render_template("login/login.html", i18n=i18n_get())


@app.route("/login/student", methods=["GET", "POST"])
@not_logged_in
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
@not_logged_in
def login_teacher():
    if request.method == "POST":
        if not helper.has_keys(["email", "password"], request.form):
            return "Illegal request: Request form requires email and password"

        email = request.form["email"]
        password = request.form["password"]

        login_help = helper.login(email, password, 1, Globals.user_id_cache, i18n_get(), "login/teacher.html")
        if login_help[0]:
            return login_help[1]

        return redirect(url_for("index"))

    return render_template("login/teacher.html", i18n=i18n_get())


@app.route("/login/personal", methods=["GET", "POST"])
@not_logged_in
def login_personal():
    if request.method == "POST":
        if not helper.has_keys(["email", "password"], request.form):
            return "Illegal request: Request form requires email and password"

        email = request.form["email"]
        password = request.form["password"]

        login_help = helper.login(email, password, 0, Globals.user_id_cache, i18n_get(), "login/personal.html")
        if login_help[0]:
            return login_help[1]

        return redirect(url_for("index"))

    return render_template("login/personal.html", i18n=i18n_get())


@app.route("/register")
@not_logged_in
def register():
    return redirect(url_for("login"))


@app.route("/register/personal", methods=["GET", "POST"])
@not_logged_in
def register_personal():
    if request.method == "POST":
        if not helper.has_keys(["email", "username", "password"], request.form):
            return "Illegal request: Request form requires email, username and password"

        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        i18n = i18n_get()
        checks = helper.register_checks(email, username, password, i18n, "register/personal.html")
        if checks[0]:
            return checks[1]

        pwd = helper.create_password(password)

        entry = db.User(
            account_type=0,
            email=email,
            username=username,
            salt=pwd[0],
            password=pwd[1],
            creation_date=helper.millis(),
            last_login_date=helper.millis(),
            xp=0,
            coins=0,
            avatar="default"
        )

        db.session.add(entry)
        db.session.commit()

        session['user_id'] = str(entry.user_id)
        Globals.user_id_cache.cache(entry)

        return redirect(url_for("index"))

    return render_template("register/personal.html", i18n=i18n_get())


@app.route("/register/teacher", methods=["GET", "POST"])
@not_logged_in
def register_teacher():
    if request.method == "POST":
        if not helper.has_keys(["email", "username", "password"], request.form):
            return "Illegal request: Request form requires email, username and password"

        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        i18n = i18n_get()
        checks = helper.register_checks(email, username, password, i18n, "register/teacher.html")
        if checks[0]:
            return checks[1]

        pwd = helper.create_password(password)

        entry = db.User(
            account_type=1,
            email=email,
            username=username,
            salt=pwd[0],
            password=pwd[1],
            creation_date=helper.millis(),
            last_login_date=helper.millis(),
            xp=0,
            coins=0,
            avatar="default_teacher"
        )

        db.session.add(entry)
        db.session.commit()

        session['user_id'] = str(entry.user_id)
        Globals.user_id_cache.cache(entry)

        return redirect(url_for("index"))

    return render_template("register/teacher.html", i18n=i18n_get())


@app.route('/panel')
@login_required
def panel():
    return render_template("panel/home.html", i18n=i18n_get())


@app.route('/account')
@login_required
def account():
    return render_template("panel/account.html", i18n=i18n_get())


@app.route('/subjects')
@login_required
def subjects():
    return redirect(url_for("specific_subject", subject_id=1))


@app.route('/subjects/<subject_id>')
@login_required
def specific_subject(subject_id: str):
    if not subject_id.isdigit():
        return "Subject ID must be a digit"

    islands = db.session.query(db.Island).filter_by(owner=g.user_db.user_id).all()

    return render_template("panel/subjects.html", i18n=i18n_get(), subjects=db.session.query(db.Subject).all(), current_subject=int(subject_id), islands=islands)


@app.route('/admin/subjects')
def admin_subject_creator():
    return render_template("admin/subject_creator.html", i18n=i18n_get(), subjects=db.session.query(db.Subject).all())


@app.route('/subject/<subject_id>/icon')
@login_required
def serverside_subject_icon(subject_id: str):
    if not subject_id.isdigit():
        return "Subject ID must be a digit"

    path = Path(f"serverside_assets/subject_data/{subject_id}/icon.png")
    if not path.exists():
        return "No assigned icon"

    return send_file(path, mimetype="image/png")


@app.route('/api/add_subject/<subject_name>')
def api_add_subject(subject_name: str):
    db.session.add(db.Subject(name=subject_name, creation_date=helper.millis()))
    db.session.commit()
    return "OK"


if __name__ == '__main__':
    app.run(debug=True)
