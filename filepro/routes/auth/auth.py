from flask import Blueprint, render_template, session, request, redirect
from filepro.utils.db_utils import get_user_data, create_user
# from filepro.utils.utils import is_logged_in
import re
from hashlib import md5

EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
auth_blueprint = Blueprint("auth_blueprint", __name__, template_folder="templates")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    errormsg = ""
    if request.method == "POST":
        data = get_user_data(request.form.get("user_identifier"))
        if data:
            password = md5(request.form.get("password").encode()).hexdigest()
            if password == data.password and data.id != "1":  # check if anonymous
                session["password"] = password
                session["username"] = data.username
                return redirect(f"/user/{data.username}")
        errormsg = "Wrong username/email or password!"
    return render_template("login.html", errormsg=errormsg)


@auth_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = md5(request.form.get("password").encode()).hexdigest()
        username = request.form.get("username")
        if not re.fullmatch(EMAIL_REGEX, email):
            return render_template("signup.html", errormsg="Please suppy a valid email!")
        if get_user_data(email):
            return render_template("signup.html", errormsg="Email already registered!")
        if len(username) < 3:
            return render_template("signup.html", errormsg="Username has to be at least 3 characters long!")
        if re.fullmatch(EMAIL_REGEX, username):
            return render_template("signup.html", errormsg="Please do not supply an email as username!")
        if get_user_data(username):
            return render_template("signup.html", errormsg="Username is already taken!")
        create_user(username, password, email)
        session["password"] = password
        session["username"] = username
        return redirect(f"/user/{username}")
    return render_template("signup.html")


@auth_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect("/")
