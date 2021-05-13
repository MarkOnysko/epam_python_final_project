# pylint: disable=C0301
"""Module contains the view functions for employees."""
from datetime import datetime

import requests as client
from flask import render_template, request, redirect, flash, url_for, abort
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


@bp.route("/employees/<int:emp_id>/edit/<int:from_dep>", methods=["GET", "POST"])
def employee_edit_view(emp_id, from_dep=0):
    """
    On GET request renders the "employees_list.html" template with
    form filled with data of the employee to edit, if invalid emp_id
    specified in url - aborts with 404 error. On form submitting validates
    the data. If validation passes - PUTs data to REST API. If response code
    is 200 redirects  with success message. Else - with error message and filled
    form. The redirect point to employees list view or to a department detail
    view, depending on where the "Edit" was requested.
    """
    response = client.get(f"{BASE_URL}/api/v1/employees/{emp_id}")
    if response.status_code == 404:
        abort(404, description=response.json()["message"])
    response_data = response.json()
    response_data["date_of_birth"] = datetime.strptime(
        response_data["date_of_birth"], "%Y-%m-%d"
    ).date()
    response_data["department_id"] = response_data["department"]["id"]
    departments = client.get(f"{BASE_URL}/api/v1/departments").json()
    form = EmployeeForm(departments, data=response_data)
    if form.validate_on_submit():
        data = {
            "name": request.form["name"],
            "date_of_birth": request.form["date_of_birth"],
            "salary": request.form["salary"],
            "department_id": request.form["department_id"],
        }
        response = client.put(f"{BASE_URL}/api/v1/employees/{emp_id}", json=data)
        if response.status_code == 200:
            flash("Employee updated successfully.")
            return (
                redirect(url_for("views.employees_list_view"))
                if not from_dep
                else redirect(
                    url_for(
                        "views.department_detail_view",
                        dep_id=data["department_id"],
                    )
                )
            )
        flash(response.json()["message"])
    employees = client.get(f"{BASE_URL}/api/v1/employees").json()
    return render_template(
        "employees_list.html",
        employees=employees,
        form=form,
        active="employees",
        emp_id=emp_id,
        from_dep=from_dep,
    )


@bp.route("/employees/<int:emp_id>/delete")
def employee_delete_view(emp_id):
    """
    Performs a delete request to REST API with the employee id.
    If response code is 404 aborts with 404 error.
    Else - redirects to the previous url.
    """
    response = client.delete(f"{BASE_URL}/api/v1/employees/{emp_id}/")
    if response.status_code == 404:
        abort(404, description=response.json()["message"])
    else:
        flash("Employee deleted successfully.")
    return redirect(request.referrer)


@bp.route("/employees/search")
@bp.route("/departments/<int:dep_id>/employees/search")
def employees_search_view(dep_id=None):
    """
    Gets the "date_of_birth" and "date_for_interval"(if provided) query
    parameters and makes a request to the REST API with them. Renders the
    "department_detail.html" or "employees_list.html" template (depending on
    where is called from) with the list of employees obtained from API.
    If invalid dep_id specified in url - aborts with 404 error.
    """
    if dep_id:
        response = client.get(f"{BASE_URL}/api/v1/departments/{dep_id}")
        if response.status_code == 404:
            abort(404, description=response.json()["message"])
        date_of_birth = request.args.get("date_of_birth")
        date_for_interval = request.args.get("date_for_interval")
        if date_for_interval:
            employees = client.get(
                f"{BASE_URL}/api/v1/departments/{dep_id}/employees/search?date_of_birth={date_of_birth}&date_for_interval={date_for_interval}"
            ).json()
        else:
            employees = client.get(
                f"{BASE_URL}/api/v1/departments/{dep_id}/employees/search?date_of_birth={date_of_birth}"
            ).json()
        return render_template(
            "department_detail.html",
            department=response.json(),
            employees=employees,
            active="departments",
            back_url=url_for(
                "views.department_detail_view", dep_id=response.json()["id"]
            ),
        )
    date_of_birth = request.args.get("date_of_birth")
    date_for_interval = request.args.get("date_for_interval")
    if date_for_interval:
        employees = client.get(
            f"{BASE_URL}/api/v1/employees/search?date_of_birth={date_of_birth}&date_for_interval={date_for_interval}"
        ).json()
    else:
        employees = client.get(
            f"{BASE_URL}/api/v1/employees/search?date_of_birth={date_of_birth}"
        ).json()
    return render_template(
        "employees_list.html",
        employees=employees,
        active="employees",
        back_url=url_for("views.employees_list_view"),
    )
