from flask import Flask
from filepro.routes import file_blueprint, general_blueprint, auth_blueprint
from werkzeug.utils import secure_filename
from pathlib import Path

# MAIN.PY
app = Flask(__name__)
app.secret_key = "J%&kBM;5(gKVU%NZHAE-82/]T[4R_r"
app.config['UPLOAD_FOLDER'] = Path(app.root_path).joinpath('database/files')
app.register_blueprint(file_blueprint)
app.register_blueprint(general_blueprint)
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
