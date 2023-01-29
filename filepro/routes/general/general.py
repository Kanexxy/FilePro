from flask import Blueprint, render_template, send_from_directory, session
from filepro.utils.utils import is_logged_in
general_blueprint = Blueprint("general_blueprint", __name__, template_folder="templates")


@general_blueprint.route("/", methods=["GET"])
def general():
    return render_template("general.html", username=session.get("username", "User"), logged=is_logged_in(session))


@general_blueprint.route("/favicon.ico", methods=["GET"])
def send_favicon():
    return send_from_directory("static", "images/favicon.png")
