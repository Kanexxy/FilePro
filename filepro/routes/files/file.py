from flask import Blueprint, render_template

file_blueprint = Blueprint("file_blueprint", __name__, template_folder="templates")

@file_blueprint.route("/files")
def open_user_dashboard():
    ...