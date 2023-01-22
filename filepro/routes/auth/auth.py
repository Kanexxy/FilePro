from flask import Blueprint, render_template, session, request, redirect
from filepro.utils.db_utils import get_user_data
from hashlib import md5

auth_blueprint = Blueprint("auth_blueprint", __name__, template_folder="templates")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    errormsg = ""
    if request.method == "POST":
        data = get_user_data(request.form.get("user_identifier"))
        password = md5(request.form.get("password").encode()).hexdigest()
        if data:
            if password == data.password:
                session["password"] = password
                session["email"] = data.email
                return redirect(f"/user/{data.username}")
        errormsg = "Wrong username/email or password!"
    return render_template("login.html", errormsg=errormsg)

@auth_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        ...
    return render_template("signup.html")
