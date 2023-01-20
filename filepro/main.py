from flask import Flask
from filepro.routes import file_blueprint, general_blueprint

app = Flask(__name__)

app.register_blueprint(file_blueprint)
app.register_blueprint(general_blueprint)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)