from flask import Blueprint, render_template

auth_blueprint = Blueprint("auth_blueprint", __name__, template_folder="templates")