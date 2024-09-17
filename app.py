from flask import Flask, render_template
from i18n import I18NEngine

app = Flask(__name__)


@app.route('/')
def index():
    engine = I18NEngine("en_us")
    engine.load()
    return render_template("index.html", i18n=engine.get)


if __name__ == '__main__':
    app.run()
