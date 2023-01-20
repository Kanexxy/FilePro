from flask import Flask
from filepro.routes.files.file import file_blueprint

app = Flask(__name__)

app.register_blueprint(file_blueprint)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/favicon.ico")
def get_favicon():
    with open("../FilePro_logo.png", "rb") as f:
        return f.read()