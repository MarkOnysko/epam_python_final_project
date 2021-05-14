# pylint: disable=W0613
# pylint: disable=C0116
"""Module contains test for DepartmentServices class's methods"""

import pytest

from department_app.service import DepartmentServices, EmployeeServices


def test_get_all(app):
    departments = DepartmentServices.get_all()
    assert len(departments) == 2


def test_get_by_id(app):
    department = DepartmentServices.get_by_id(1)
    assert department is not None
    assert department.name == "Dep 1"


def test_get_by_wrong_id(app):
    department = DepartmentServices.get_by_id(42)
    assert department is None


def test_create(app):
    department = DepartmentServices.create(dict(name="Dep 3"))
    departments = DepartmentServices.get_all()
    assert department.name == "Dep 3"
    assert len(departments) == 3
    assert department in departments


def test_create_wrong_data(app):
    with pytest.raises(TypeError):
        DepartmentServices.create(dict(title="Dep 3"))


def test_update(app):
    department_to_update = DepartmentServices.get_by_id(1)
    updated = DepartmentServices.update(
        department_to_update, dict(name="Updated dep 1")
    )
    departments = DepartmentServices.get_all()
    assert updated.name == "Updated dep 1"
    assert len(departments) == 2


def test_delete(app):
    department_to_delete = DepartmentServices.get_by_id(1)
    DepartmentServices.delete(department_to_delete)
    departments = DepartmentServices.get_all()
    employees = EmployeeServices.get_all()
    assert department_to_delete not in departments
    assert len(departments) == 1
    # to check if cascade delete happened
    assert len(employees) == 3


def test_avg_salary_non_empty_departments(app):
    dep_1 = DepartmentServices.get_by_id(1)
    dep_2 = DepartmentServices.get_by_id(2)
    salary_1 = DepartmentServices.get_avg_salary(dep_1)
    salary_2 = DepartmentServices.get_avg_salary(dep_2)
    assert salary_1 == 1000
    assert salary_2 == 2000


def test_avg_salary_empty_department(app):
    dep_3 = DepartmentServices.create(dict(name="Dep 3"))
    salary_3 = DepartmentServices.get_avg_salary(dep_3)
    assert salary_3 == 0
