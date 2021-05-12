# pylint: disable=C0413
"""Module contains the definition of the blueprint for views."""
from flask import Blueprint

bp = Blueprint("views", __name__, template_folder="templates")
from department_app.views import department_views, employees_views
