from flask import Flask, render_template
from cache import Globals

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", i18n=Globals.i18n_cache.get_or_create("en_us").get)


if __name__ == '__main__':
    app.run()
