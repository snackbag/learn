from flask import Flask, render_template
from cache import Globals

app = Flask(__name__)


def i18n_get(lang: str):
    return Globals.i18n_cache.get_or_create(lang).get


@app.route('/')
def index():
    return render_template("index.html", i18n=i18n_get("en_us"))

@app.route("/login")
def login():
    return render_template("login.html", i18n=i18n_get())


if __name__ == '__main__':
    app.run()
