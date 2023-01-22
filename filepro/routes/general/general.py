from flask import Blueprint, render_template, send_from_directory

general_blueprint = Blueprint("general_blueprint", __name__, template_folder="templates")


@general_blueprint.route("/")
def general():
    return render_template("general.html")


@general_blueprint.route("/favicon.ico", methods=["GET"])
def send_favicon():
    return send_from_directory("static", "images/favicon.png")
