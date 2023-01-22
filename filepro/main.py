from flask import Flask
from filepro.routes import file_blueprint, general_blueprint, auth_blueprint

app = Flask(__name__)
app.secret_key = "wblu8gatkmb2mp3ymnf0"
app.register_blueprint(file_blueprint)
app.register_blueprint(general_blueprint)
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
