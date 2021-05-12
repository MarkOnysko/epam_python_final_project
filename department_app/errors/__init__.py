# pylint: disable=C0413
"""Module contains the definition of the blueprint for errorhandlers."""
from flask import Blueprint

bp = Blueprint("errors", __name__, template_folder="templates")
from department_app.errors import handlers
