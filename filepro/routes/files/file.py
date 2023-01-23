from flask import Blueprint, render_template, session, redirect
from filepro.utils.utils import is_logged_in
file_blueprint = Blueprint("file_blueprint", __name__, template_folder="templates")


@file_blueprint.route("/user/<username>")
def open_user_dashboard(username):
    if not is_logged_in(session) or session.get("username") != username:
        print(session, is_logged_in(session))
        return redirect("/login")
    return f"<h1>Dashboard from {username}</h1>"
