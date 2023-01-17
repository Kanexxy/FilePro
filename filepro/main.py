from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/favicon.ico")
def get_favicon():
    with open("../FilePro_logo.png", "rb") as f:
        return f.read()