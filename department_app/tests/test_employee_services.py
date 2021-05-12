""""Module contains test for EmployeeServices class's methods"""
from datetime import date
import pytest
from sqlalchemy.exc import IntegrityError
from department_app.service import EmployeeServices


def test_get_all(app):
    employees = EmployeeServices.get_all()
    assert len(employees) == 5


def test_get_all_for_department(app):
    dep_1_employees = EmployeeServices.get_all_for_department(1)
    dep_2_employees = EmployeeServices.get_all_for_department(2)
    dep_3_employees = EmployeeServices.get_all_for_department(3)
    assert len(dep_1_employees) == 2
    assert len(dep_2_employees) == 3
    assert len(dep_3_employees) == 0


def test_get_by_valid_id(app):
    emp_1 = EmployeeServices.get_by_id(1)
    assert emp_1 is not None
    assert emp_1.name == "Employee 1"


def test_get_by_invalid_id(app):
    emp_1 = EmployeeServices.get_by_id(42)
    assert emp_1 is None


def test_get_by_date_of_birth_without_interval(app):
    test_date = date(1991, 1, 1)
    employees = EmployeeServices.get_by_date_of_birth(test_date)
    assert all(emp.date_of_birth == test_date for emp in employees)


def test_get_by_date_of_birth_with_interval(app):
    test_date1 = date(1991, 1, 1)
    test_date2 = date(1993, 3, 3)
    employees = EmployeeServices.get_by_date_of_birth(test_date1, test_date2)
    assert all(test_date1 <= emp.date_of_birth <= test_date2 for emp in employees)


def test_get_by_date_of_birth_from_department_without_interval(app):
    dep_id = 1
    test_date = date(1991, 1, 1)
    employees = EmployeeServices.get_by_date_of_birth_from_department(dep_id, test_date)
    assert all(emp.date_of_birth == test_date for emp in employees)
    assert all(emp.department_id == dep_id for emp in employees)


def test_get_by_date_of_birth_from_department_with_interval(app):
    dep_id = 1
    test_date1 = date(1991, 1, 1)
    test_date2 = date(2000, 1, 1)
    employees = EmployeeServices.get_by_date_of_birth_from_department(
        dep_id, test_date1, test_date2
    )
    assert all(test_date1 <= emp.date_of_birth <= test_date2 for emp in employees)
    assert all(emp.department_id == dep_id for emp in employees)


def test_create(app):
    new_employee = EmployeeServices.create(
        dict(
            name="New Employee",
            date_of_birth=date(1999, 9, 9),
            salary=3000,
            department_id=1,
        )
    )
    employees = EmployeeServices.get_all()
    assert new_employee.name == "New Employee"
    assert len(employees) == 6
    assert new_employee in employees


def test_create_incomplete_data(app):
    with pytest.raises(IntegrityError):
        EmployeeServices.create(
            dict(
                name="New Employee",
                salary=3000,
                department_id=1,
            )
        )


def test_create_wrong_data(app):
    with pytest.raises(TypeError):
        EmployeeServices.create(
            dict(
                name="New Employee",
                birthday=date(1999, 9, 9),
                salary=3000,
                department_id=1,
            )
        )


def test_create_non_existent_department_id(app):
    with pytest.raises(IntegrityError):
        EmployeeServices.create(
            dict(
                name="New Employee",
                date_of_birth=date(1999, 9, 9),
                salary=3000,
                department_id=42,
            )
        )


def test_update(app):
    employee_to_update = EmployeeServices.get_by_id(1)
    updated = EmployeeServices.update(
        employee_to_update,
        dict(
            name="Updated Employee",
            department_id=2,
        ),
    )
    employees = EmployeeServices.get_all()
    assert updated.name == "Updated Employee"
    assert updated.department_id == 2
    assert updated.salary == employee_to_update.salary
    assert len(employees) == 5
    assert updated in employees


def test_delete(app):
    employee_to_delete = EmployeeServices.get_by_id(1)
    EmployeeServices.delete(employee_to_delete)
    employees = EmployeeServices.get_all()
    assert employee_to_delete not in employees
    assert len(employees) == 4
