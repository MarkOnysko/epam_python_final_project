"""Module contains Flask-Restful Resources for Departments"""
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from department_app.service import DepartmentServices, EmployeeServices
from .schemas import DepartmentSchema, EmployeeSchema


class DepartmentsAPI(Resource):
    """
    This class defines the DepartmentsAPI Resource, available at the
    "/api/v1/departments/[<int:id>]" url
    """

    department_schema = DepartmentSchema()

    def get(self, dep_id=None):
        """
        This method is called when GET request is sent to "/api/v1/departments/[<int:id>]" url
        :return: if "id" not specified the list of all departments in json format,
        status code 200. If id specified -  the department with the specified id
        serialized to json. If invalid id - error message and status code 404.
        """
        if not dep_id:
            departments = DepartmentServices.get_all()
            return self.department_schema.dump(departments, many=True), 200
        department = DepartmentServices.get_by_id(dep_id)
        if not department:
            return {"message": f"Department with id {dep_id} not found"}, 404
        return self.department_schema.dump(department), 200

    def post(self):
        """
        This method is called when POST request is sent to url "/api/v1/departments"
         with json data. Creates a new department entry in database.
        :return: if valid data provided returns the created entry serialized
        to json, status code 201, if invalid data - returns the error massage
        in json format, status code 400.
        """
        json_data = request.get_json(force=True)
        try:
            data = self.department_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 400
        try:
            new_department = DepartmentServices.create(data)
        except IntegrityError:
            return {"message": "Department names should be unique."}, 400
        return self.department_schema.dump(new_department), 201

    def put(self, dep_id):
        """
        This method is called when PUT request is sent to url "/api/v1/departments/id"
        with json data, updates the department entry with specified id in database.
        :return: if valid data provided returns the updated entry serialized
        to json, status code 200, if invalid data - returns the error massage
        in json format, status code 400. If invalid id specified - returns error
        message and status code 404.
        """
        json_data = request.get_json(force=True)
        department = DepartmentServices.get_by_id(dep_id)
        if not department:
            return {"message": f"Department with id {dep_id} not found"}, 404
        try:
            data = self.department_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 400
        try:
            department = DepartmentServices.update(department, data)
        except IntegrityError:
            return {"message": "Department names should be unique."}, 400
        return self.department_schema.dump(department), 200

    def patch(self, dep_id):
        """
        This method is called when PATCH request is sent to url "/api/v1/departments/id"
        with json data, updates the department entry with specified id in database.
        :return: if valid data provided returns the updated entry serialized
        to json, status code 200, if invalid data - returns the error massage
        in json format, status code 400. If invalid id specified - returns error
        message and status code 404.
        """
        json_data = request.get_json(force=True)
        department = DepartmentServices.get_by_id(dep_id)
        if not department:
            return {"message": f"Department with id {dep_id} not found"}, 404
        try:
            data = self.department_schema.load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 400
        try:
            department = DepartmentServices.update(department, data)
        except IntegrityError:
            return {"message": "Department names should be unique."}, 400
        return self.department_schema.dump(department), 200

    @staticmethod
    def delete(dep_id):
        """
        This method is called when DELETE request is sent to url "/api/v1/departments/id"
        deletes the department entry with specified id from database.
        :return: returns an empty response body and status code 204 if valid id
        specified. If invalid id specified - returns error message and status code 404.
        """
        department = DepartmentServices.get_by_id(dep_id)
        if not department:
            return {"message": f"Department with id {dep_id} not found"}, 404
        DepartmentServices.delete(department)
        return "", 204


class DepartmentsEmployeesAPI(Resource):
    """
    This class defines the DepartmentsEmployeesAPI Resource,
    available at the "/api/v1/departments/<int:dep_id>/employees" url.
    """

    employee_schema = EmployeeSchema()

    def get(self, dep_id):
        """
        This method is called when GET request is sent to
        "/api/v1/departments/<int:dep_id>/employees" url.
        :return: return the json-serialized list of employees working in
        department with id specified in url, status code 200. If invalid id -
        error message and status code 404.
        """
        department = DepartmentServices.get_by_id(dep_id)
        if not department:
            return {"message": f"Department with id {dep_id} not found"}, 404
        employees = EmployeeServices.get_all_for_department(dep_id)
        return self.employee_schema.dump(employees, many=True), 200

    def post(self, dep_id):
        """
        This method is called when POST request is sent to url
        "/api/v1/departments/<int:dep_id>/employees" with json data.
        Creates a new employee entry in database with department_id=dep_id.
        :return: if valid data provided returns the created entry serialized
        to json, status code 201, if invalid data - returns the error massage
        in json format, status code 400. If invalid department id specified in url -
        returns not-found error message, status code 404.
        """
        department = DepartmentServices.get_by_id(dep_id)
        if not department:
            return {"message": f"Department with id {dep_id} not found"}, 404
        json_data = request.get_json(force=True)
        try:
            data = self.employee_schema.load(json_data, partial=["department_id"])
        except ValidationError as e:
            return {"message": e.messages}, 400
        data["department_id"] = dep_id
        try:
            new_employee = EmployeeServices.create(data)
        except IntegrityError:
            return {"message": "Not valid department id"}, 400
        return self.employee_schema.dump(new_employee), 201
