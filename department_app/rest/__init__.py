"""
Module contains the definition of the Flask-Restful API instance
and the routing for the REST-API Resources.
"""
from flask_restful import Api

from department_app.rest.department_resourses import (
    DepartmentsAPI,
    DepartmentsEmployeesAPI,
)
from department_app.rest.employee_resources import EmployeesAPI, EmployeesSearchAPI

api = Api(
    prefix="/api/v1",
)

api.add_resource(
    DepartmentsAPI,
    "/departments",
    methods=["GET", "POST"],
    endpoint="departments",
    strict_slashes=False,
)

api.add_resource(
    DepartmentsAPI,
    "/departments/<dep_id>",
    methods=["GET", "PUT", "PATCH", "DELETE"],
    endpoint="department",
    strict_slashes=False,
)

api.add_resource(
    DepartmentsEmployeesAPI,
    "/departments/<dep_id>/employees",
    methods=["GET", "POST"],
    strict_slashes=False,
)



api.add_resource(
    EmployeesAPI,
    "/employees",
    methods=["GET", "POST"],
    endpoint="employees",
    strict_slashes=False,
)

api.add_resource(
    EmployeesAPI,
    "/employees/<emp_id>",
    methods=["GET", "PUT", "PATCH", "DELETE"],
    endpoint="employee",
    strict_slashes=False,
)

api.add_resource(
    EmployeesSearchAPI,
    "/employees/search",
    "/departments/<dep_id>/employees/search",
    methods=["GET"],
    strict_slashes=False,
)
