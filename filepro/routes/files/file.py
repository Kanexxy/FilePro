from flask import Blueprint, render_template, session, redirect, request, current_app, send_from_directory
from filepro.utils.utils import is_logged_in, get_file_suffix
from filepro.utils.db_utils import get_user_data, register_file, get_file_name
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
file_blueprint = Blueprint("file_blueprint", __name__, template_folder="templates")


@file_blueprint.route("/user/<username>")
def open_user_dashboard(username):
    if not is_logged_in(session) or session.get("username") != username:
        print(session, is_logged_in(session))
        return redirect("/login")

    return render_template("dashboard.html")


@file_blueprint.route("/anonupload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return {"error": "no file transmitted"}
    file = request.files['file']
    if file.filename == '':
        return {"error": "no file selected"}
    if file:
        old_filename = secure_filename(file.filename)
        new_filename = f"{uuid4()}{get_file_suffix(old_filename)}"
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))
        register_file(new_filename, old_filename, get_user_data("anonymous").id)
        return {
            "filename": old_filename,
            "uuid_filename": new_filename,
            "full_url": f"{request.host_url}file/{new_filename}"
        }
    return redirect("/")


@file_blueprint.route("/file/<uuid>")
def anon_download(uuid):
    names = get_file_name(uuid)
    print(names)
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'], names.uuid, download_name=names.filename
    )
