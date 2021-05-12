# pylint: disable=C0103
"""
Module contains Flask-Restful Resources for Employees
and for EmployeesSearch.
"""
from datetime import datetime
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from department_app.service import EmployeeServices, DepartmentServices
from .schemas import EmployeeSchema


class EmployeesAPI(Resource):
    """
    This class defines the EmployeesAPI Resource, available at the
    "/api/v1/employees/[<int:id>]" url
    """

    employee_schema = EmployeeSchema()

    def get(self, emp_id=None):
        """
        This method is called when GET request is sent to
        "/api/v1/employees/[<int:id>]" url.
        :return: if "id" not specified the list of all employees in json format,
        status code 200. If id specified -  the employee with the specified id
        serialized to json. If invalid id - error message and status code 404.
        """
        if not emp_id:
            employees = EmployeeServices.get_all()
            return self.employee_schema.dump(employees, many=True), 200
        employee = EmployeeServices.get_by_id(emp_id)
        if not employee:
            return {"message": f"Employee with id {emp_id} not found"}, 404
        return self.employee_schema.dump(employee), 200

    def post(self):
        """
        This method is called when POST request is sent to url "/api/v1/employees"
         with json data. Creates a new employee entry in database.
        :return: if valid data provided returns the created entry serialized
        to json, status code 201, if invalid data - returns the error massage
        in json format, status code 400.
        """
        json_data = request.get_json(force=True)
        try:
            data = self.employee_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 400
        try:
            new_employee = EmployeeServices.create(data)
        except IntegrityError:
            return {"message": "Not valid department id"}, 400
        return self.employee_schema.dump(new_employee), 201

    def put(self, emp_id):
        """
        This method is called when PUT request is sent to url "/api/v1/employees/id"
        with json data, updates the employee entry with specified id in database.
        :return: if valid data provided returns the updated entry serialized
        to json, status code 200, if invalid data - returns the error massage
        in json format, status code 400. If invalid id specified - returns error
        message and status code 404.
        """
        employee = EmployeeServices.get_by_id(emp_id)
        if not employee:
            return {"message": f"Employee with id {emp_id} not found"}, 404
        json_data = request.get_json(force=True)
        try:
            data = self.employee_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 400
        try:
            employee = EmployeeServices.update(employee, data)
        except IntegrityError:
            return {"message": "Not valid department id"}, 400
        return self.employee_schema.dump(employee), 200

    def patch(self, emp_id):
        """
        This method is called when PATCH request is sent to url "/api/v1/employees/id"
        with json data, updates(also with incomplete data) the employee entry
        with specified id in database.
        :return: if valid data provided returns the updated entry serialized
        to json, status code 200, if invalid data - returns the error massage
        in json format, status code 400. If invalid id specified - returns error
        message and status code 404.
        """
        employee = EmployeeServices.get_by_id(emp_id)
        if not employee:
            return {"message": f"Employee with id {emp_id} not found"}, 404
        json_data = request.get_json(force=True)
        try:
            data = self.employee_schema.load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 400
        try:
            employee = EmployeeServices.update(employee, data)
        except IntegrityError:
            return {"message": "Not valid department id"}, 400
        return self.employee_schema.dump(employee), 200

    @staticmethod
    def delete(emp_id):
        """
        This method is called when DELETE request is sent to url "/api/v1/employees/id"
        deletes the employee entry with specified id from database.
        :return: returns an empty response body and status code 204 if valid id
        specified. If invalid id specified - returns error message and status code 404.
        """
        employee = EmployeeServices.get_by_id(emp_id)
        if not employee:
            return {"message": f"Employee with id {emp_id} not found"}, 404
        EmployeeServices.delete(employee)
        return "", 204


class EmployeesSearchAPI(Resource):
    """
    This class defines the EmployeesSearchAPI Resource, available at urls
    "/api/v1/employees/search",
    "/api/v1//departments/<dep_id>/employees/search"
    """

    employee_schema = EmployeeSchema()

    def get(self, dep_id=None):
        """
        This method is called when GET request is sent to
        "/api/v1/employees/search" or
        "/api/v1//departments/<dep_id>/employees/search" urls.
        The method parses the "date_of_birth" and(optional) "date_for_interval"
        query parameters from the GET request, and based on them filters out
        the employees born on a specified date or in an interval between dates.
        Depending on url fetches employees for a specific department or all.
        :return: if sent to "/api/v1/employees/search" returns the list all
        employees born on a specified date or in an interval between dates in json format,
        status code 200. if sent to "/api/v1//departments/<dep_id>/employees/search" -
        the same but only for employees from specified department.
        If no "date_of_birth" parameter provided - returns error message, status code 400.
        If invalid department id provided - returns error message, status code 404.
        """
        date_of_birth = request.args.get("date_of_birth")
        if not date_of_birth:
            return {"message": "Enter search data"}, 400
        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        date_for_interval = request.args.get("date_for_interval")
        if date_for_interval:
            date_for_interval = datetime.strptime(date_for_interval, "%Y-%m-%d").date()
        if not dep_id:
            employees = EmployeeServices.get_by_date_of_birth(
                date_of_birth, date_for_interval
            )
        else:
            department = DepartmentServices.get_by_id(dep_id)
            if not department:
                return {"message": f"Department with id {dep_id} not found"}, 404
            employees = EmployeeServices.get_by_date_of_birth_from_department(
                dep_id, date_of_birth, date_for_interval
            )
        return self.employee_schema.dump(employees, many=True), 200
