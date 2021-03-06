# pylint: disable=C0301
"""Module contains the view functions for departments."""
import requests as client
from flask import render_template, request, redirect, flash, url_for, abort
from department_app.forms import DepartmentForm, EmployeeForm
from department_app.views import bp

BASE_URL = "http://127.0.0.1:5000"


@bp.route("/", methods=["GET", "POST"])
@bp.route("/departments", methods=["GET", "POST"])
def departments_list_view():
    """
    On GET request obtains the list of departments from the REST-API and renders the
    "departments_list.html" template with form to create a new department.
    On form submission validates the form data, if validation fails rerenders
    the template with error messages. If valid data send in in a post request to the REST-API.
    If it returns status code 201 redirects to self and flashes a success message,
    else flashes the API-sent error message.
    """
    form = DepartmentForm()
    if form.validate_on_submit():
        data = {"name": request.form["name"]}
        response = client.post(f"{BASE_URL}/api/v1/departments", json=data)
        if response.status_code == 201:
            flash("Department created successfully.")
        else:
            flash(response.json()["message"])
        return redirect(url_for("views.departments_list_view"))
    departments = client.get(f"{BASE_URL}/api/v1/departments").json()
    return render_template(
        "departments_list.html",
        departments=departments,
        active="departments",
        form=form,
    )


@bp.route("/departments/<int:dep_id>")
def department_detail_view(dep_id):
    """
    Renders the "department_detail.html" template, with the list of employees
    working in the specified department and a form to add employees to it.
    If invalid dep_id passed in the url - aborts with 404 error.
    """
    departments = client.get(f"{BASE_URL}/api/v1/departments").json()
    form = EmployeeForm(departments)
    response = client.get(f"{BASE_URL}/api/v1/departments/{dep_id}")
    if response.status_code == 404:
        abort(404, description=response.json()["message"])
    employees = client.get(f"{BASE_URL}/api/v1/departments/{dep_id}/employees").json()
    return render_template(
        "department_detail.html",
        department=response.json(),
        employees=employees,
        active="departments",
        form=form,
        back_url=url_for("views.departments_list_view"),
    )


@bp.route("/departments/<int:dep_id>/employees", methods=["POST"])
def create_employee_for_department(dep_id):
    """Processes the form submission in "department_detail.html", validates the date,
    if invalid - redirects back with validation errors. If valid adds to the data
    the department id and  posts it to the REST API. If response status code is 201 -
    redirects to department_detail view with success massage. Else redirects with error
    message and the prefilled form.
    """
    departments = client.get(f"{BASE_URL}/api/v1/departments").json()
    form = EmployeeForm(departments, request.form, department_id=dep_id)
    if form.validate():
        data = {
            "name": request.form["name"],
            "date_of_birth": request.form["date_of_birth"],
            "salary": request.form["salary"],
            "department_id": dep_id,
        }
        response = client.post(
            f"{BASE_URL}/api/v1/departments/{dep_id}/employees", json=data
        )
        if response.status_code == 201:
            flash("Employee created successfully")
            return redirect(url_for("views.department_detail_view", dep_id=dep_id))
        flash(response.json()["message"])
    department = client.get(f"{BASE_URL}/api/v1/departments/{dep_id}").json()
    employees = client.get(f"{BASE_URL}/api/v1/departments/{dep_id}/employees").json()
    return render_template(
        "department_detail.html",
        department=department,
        employees=employees,
        active="departments",
        form=form,
        back_url=url_for("views.departments_list_view"),
    )


@bp.route("/departments/<int:dep_id>/edit", methods=["GET", "POST"])
def department_edit(dep_id):
    """
    On GET request renders the "departments_list.html" template with
    form filled with data of the department to edit, if invalid dep_id
    specified in url - aborts with 404 error. On form submitting validates
    the data. If validation passes - PUTs data to REST API. If response code
    is 200 redirects to departments_list_view with success message. Else -
    with error message and filled form.
    """
    response = client.get(f"{BASE_URL}/api/v1/departments/{dep_id}")
    if response.status_code == 404:
        abort(404, description=response.json()["message"])
    form = DepartmentForm(data=response.json())
    if form.validate_on_submit():
        data = {"name": request.form["name"]}
        response = client.put(f"{BASE_URL}/api/v1/departments/{dep_id}", json=data)
        if response.status_code == 200:
            flash("Department updated successfully.")
            return redirect(url_for("views.departments_list_view"))
        flash(response.json()["message"])
    departments = client.get(f"{BASE_URL}/api/v1/departments").json()
    return render_template(
        "departments_list.html",
        departments=departments,
        active="departments",
        form=form,
    )


@bp.route("/departments/<int:dep_id>/delete")
def department_delete(dep_id):
    """
    Performs a delete request to REST API with the department id.
    If response code is 404 aborts with 404 error.
    Else - redirects to departments_list_view with "deleted successfully"
    message.
    """
    response = client.delete(f"{BASE_URL}/api/v1/departments/{dep_id}")
    if response.status_code == 404:
        abort(404, description=response.json()["message"])
    else:
        flash("Department deleted successfully.")
    return redirect(url_for("views.departments_list_view"))
