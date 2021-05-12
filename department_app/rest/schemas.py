# pylint: disable=R0903
# pylint: disable=R0201
"""Module contains serializer schemas for Department and Employee classes."""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate
from department_app.models import Department, Employee
from department_app.service import DepartmentServices


class DepartmentSchema(SQLAlchemyAutoSchema):
    """
    Marshmallow-SQLAlchemy schema for serializing/deserializing
    department related data.
    """

    name = fields.Str(required=True, validate=[validate.Length(min=4, max=50)])
    employees = fields.List(
        fields.Nested("EmployeeSchema", exclude=["department"]), dump_only=True
    )
    avg_salary = fields.Method("get_avg_salary")

    class Meta:
        """Metaclass for DepartmentSchema"""

        model = Department

    def get_avg_salary(self, obj):
        """
        A method to add the calculated average salary data
        to the serialized data on the fly.
        """
        return DepartmentServices.get_avg_salary(obj)


class EmployeeSchema(SQLAlchemyAutoSchema):
    """
    Marshmallow-SQLAlchemy schema for serializing/deserializing
    employee related data.
    """

    name = fields.Str(required=True, validate=[validate.Length(min=4, max=100)])
    salary = fields.Int(required=True, validate=[validate.Range(min=1)])
    department_id = fields.Int(required=True, load_only=True)
    department = fields.Nested(DepartmentSchema, dump_only=True, exclude=["employees"])

    class Meta:
        """Metaclass for EmployeeSchema"""

        model = Employee
