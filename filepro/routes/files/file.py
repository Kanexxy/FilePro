from flask import Blueprint, render_template

file_blueprint = Blueprint("file_blueprint", __name__, template_folder="templates")


@file_blueprint.route("/user/<username>")
def open_user_dashboard(username):
    return f"<h1>Dashboard from {username}</h1>"
