import os
from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    current_app,
    send_from_directory,
    abort,
)
from filepro.utils.utils import is_logged_in, get_file_suffix
from filepro.utils.db_utils import (
    get_user_data,
    register_file,
    get_file_data,
    get_user_files,
    set_file_is_public,
    delete_file_db,
)
from werkzeug.utils import secure_filename
from pathlib import Path
from uuid import uuid4

file_blueprint = Blueprint("file_blueprint", __name__, template_folder="templates")


@file_blueprint.route("/user/<url_username>")
def open_user_dashboard(url_username):
    username = session.get("username")
    if not is_logged_in(session) or session.get("username") != url_username:
        print(session, is_logged_in(session))
        return redirect("/login")

    return render_template(
        "dashboard.html", files=get_user_files(username), username=username
    )


@file_blueprint.route("/anonupload", methods=["POST"])
def anon_upload():
    if "file" not in request.files:
        return {"error": "no file transmitted"}
    file = request.files["file"]
    if file.filename == "":
        return {"error": "no file selected"}
    if file:
        old_filename = secure_filename(file.filename)
        new_filename = f"{uuid4()}{get_file_suffix(old_filename)}"
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], new_filename))
        register_file(new_filename, old_filename, get_user_data("anonymous").id, 1)
        return {
            "filename": old_filename,
            "uuid_filename": new_filename,
            "full_url": f"{request.host_url}file/{new_filename}",
        }
    return redirect("/")


@file_blueprint.route("/userupload", methods=["POST"])
def user_upload():
    if not is_logged_in(session):
        return {"error": "Please log in first."}
    if "file" not in request.files:
        return {"error": "no file transmitted"}
    file = request.files["file"]
    if file.filename == "":
        return {"error": "no file selected"}
    if file:
        username = session.get("username")
        old_filename = secure_filename(file.filename)
        new_filename = f"{uuid4()}{get_file_suffix(old_filename)}"
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], new_filename))
        register_file(new_filename, old_filename, get_user_data(username).id, 0)
        return {
            "filename": old_filename,
            "uuid_filename": new_filename,
            "full_url": f"{request.host_url}user/{username}/file/{new_filename}",
        }
    return redirect("/")


@file_blueprint.route("/file/<uuid>")
def anon_download(uuid):
    filedata = get_file_data(uuid)
    if not filedata:
        redirect("/")
    if filedata.userid != 1:
        return redirect("/login")

    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        filedata.uuid,
        download_name=filedata.filename,
        as_attachment=True,
    )


@file_blueprint.route("/user/<username>/file/<uuid>")
def user_download(username, uuid):
    filedata = get_file_data(uuid)
    if not filedata:
        redirect("/")
    if not filedata.is_public:
        if not is_logged_in(session):
            return redirect("/login")
        if filedata.userid != get_user_data(session.get("username")).id:
            return redirect("/login")
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        filedata.uuid,
        download_name=filedata.filename,
        as_attachment=True,
    )


@file_blueprint.route("/user/file/<uuid>/set_status/<status>")
def set_file_publicity(uuid, status):
    filedata = get_file_data(uuid)
    userid = get_user_data(session.get("username")).id
    if not filedata:
        return abort(404)
    if not (is_logged_in(session) and filedata.userid == userid):
        return abort(403)

    if status == "private":
        set_file_is_public(uuid, 0)
    elif status == "public":
        set_file_is_public(uuid, 1)
    else:
        return abort(400)

    return "Success", 200


@file_blueprint.route("/delete/<uuid>")
def delete_file(uuid):
    filedata = get_file_data(uuid)
    userdata = get_user_data(session.get("username"))
    if not filedata:
        return abort(400)
    if not (is_logged_in(session) and filedata.userid == userdata.id):
        return abort(403)
    delete_file_db(uuid)
    file_path = Path(current_app.config["UPLOAD_FOLDER"]) / uuid
    file_path.unlink()
    return redirect(f"/user/{userdata.username}")
