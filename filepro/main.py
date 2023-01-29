from flask import Flask
from filepro.routes import file_blueprint, general_blueprint, auth_blueprint
from werkzeug.utils import secure_filename
from pathlib import Path

# MAIN.PY
app = Flask(__name__)
app.secret_key = "J%&kBM;5(gKVU%NZHAE-82/]T[4R_r"
upload_folder_path = Path(app.root_path).joinpath('database/files');
upload_folder_path.mkdir(exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder_path
app.register_blueprint(file_blueprint)
app.register_blueprint(general_blueprint)
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(debug=True)