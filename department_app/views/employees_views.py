# pylint: disable=C0301
"""Module contains the view functions for employees."""
import requests as client
from flask import render_template, request, redirect, flash, url_for
from department_app.forms import EmployeeForm
from department_app.views import bp

BASE_URL = "http://127.0.0.1:5000"


@bp.route("/employees", methods=["GET", "POST"])
def employees_list_view():
    """
    On GET request obtains the list of employees from the REST-API and renders the
    "employees_list.html" template with form to create a new employee.
    On form submission validates the form data, if validation fails rerenders
    the template with error messages. If valid data send in in a post request to the REST-API.
    If it returns status code 201 redirects to self and flashes a success message,
    else flashes the API-sent error message.
    """
    departments = client.get(f"{BASE_URL}/api/v1/departments").json()
    form = EmployeeForm(departments)
    if form.validate_on_submit():
        data = {
            "name": request.form["name"],
            "date_of_birth": request.form["date_of_birth"],
            "salary": request.form["salary"],
            "department_id": request.form["department_id"],
        }
        response = client.post(f"{BASE_URL}/api/v1/employees", json=data)
        if response.status_code == 201:
            flash("Employee created successfully")
            return redirect(url_for("views.employees_list_view"))
        flash(response.json()["message"])
    employees = client.get(f"{BASE_URL}/api/v1/employees").json()
    return render_template(
        "employees_list.html", employees=employees, active="employees", form=form
    )