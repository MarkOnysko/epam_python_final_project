# pylint: disable=W0613
# pylint: disable=C0116
"""Module contains test for employees_views.py functions"""


def test_employees_list_view_get(module_app, mclient, server):
    response = mclient.get("/employees")
    assert response.status_code == 200
    assert b"Employees" in response.data


def test_employees_list_view_post(module_app, mclient, server):
    data = {
        "name": "New Employee",
        "date_of_birth": "1999-05-04",
        "salary": 555,
        "department_id": 1,
    }
    response = mclient.post("/employees", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"created successfully" in response.data


def test_employees_list_view_post_wrong_data(module_app, mclient, server):
    data = {
        "name": "E",
        "date_of_birth": "1999-05-04",
        "salary": 555,
        "department_id": 2,
    }
    response = mclient.post("/employees", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Field must be between 4 and 100 characters long." in response.data


def test_employee_edit_view_get(module_app, mclient, server):
    response = mclient.get("/employees/1/edit/0")
    assert response.status_code == 200


def test_employee_edit_view_get_wrong_id(module_app, mclient, server):
    response = mclient.get("/employees/42/edit/0")
    assert response.status_code == 404
    assert b"id 42 not found" in response.data


def test_employee_edit_view_post(module_app, mclient, server):
    data = {
        "name": "Employee 1 Update",
        "date_of_birth": "1999-05-04",
        "salary": 90000,
        "department_id": 1,
    }
    response = mclient.post("/employees/1/edit/0", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"updated successfully" in response.data


def test_employee_edit_view_post_fails_validation(module_app, mclient, server):
    data = {
        "name": "E",
        "date_of_birth": "1999-05-04",
        "salary": 555,
        "department_id": 2,
    }
    response = mclient.post("/employees/1/edit/0", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Field must be between 4 and 100 characters long." in response.data


def test_department_delete_view_get(module_app, mclient, server):
    response = mclient.get("/employees/1/delete")
    assert response.status_code == 302


def test_employee_delete_view_get_wrong_id(module_app, mclient, server):
    response = mclient.get("/employees/42/delete")
    assert response.status_code == 404
    assert b"id 42 not found" in response.data


def test_employees_search_view_without_dep_id_one_date(module_app, mclient, server):
    response = mclient.get("/employees/search?date_of_birth=1994-04-05")
    assert response.status_code == 200
    assert b"Employees" in response.data


def test_employees_search_view_without_dep_id_two_dates(module_app, mclient, server):
    response = mclient.get(
        "/employees/search?date_of_birth=1994-04-05&date_for_interval=2000-01-01"
    )
    assert response.status_code == 200
    assert b"Employees" in response.data


def test_employees_search_view_with_dep_id_one_date(module_app, mclient, server):
    response = mclient.get("/departments/1/employees/search?date_of_birth=1994-04-05")
    assert response.status_code == 200
    assert b"Employees" in response.data


def test_employees_search_view_with_dep_id_two_dates(module_app, mclient, server):
    response = mclient.get(
        "/departments/1/employees/search?date_of_birth=1994-04-05&date_for_interval=2000-01-01"
    )
    assert response.status_code == 200
    assert b"Employees" in response.data


def test_employees_search_view_with_invalid_dep_id_two_dates(
    module_app, mclient, server
):
    response = mclient.get(
        "/departments/42/employees/search?date_of_birth=1994-04-05&date_for_interval=2000-01-01"
    )
    assert response.status_code == 404
    assert b"id 42 not found" in response.data
