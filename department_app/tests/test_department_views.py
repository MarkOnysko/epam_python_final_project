# pylint: disable=W0613
# pylint: disable=C0116
"""Module contains test for department_views.py functions"""


def test_departments_list_view_get(module_app, mclient, server):
    response = mclient.get("/departments")
    assert response.status_code == 200
    assert b"Departments" in response.data


def test_departments_list_view_post(module_app, mclient, server):
    data = {"name": "Dep 3"}
    response = mclient.post("/departments", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"created successfully" in response.data


def test_departments_list_view_post_wrong_data(module_app, mclient, server):
    data = {"name": "De"}
    response = mclient.post("/departments", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"must be between 4 and 50 characters long" in response.data


def test_department_detail_view_get(module_app, mclient, server):
    response = mclient.get("/departments/1")
    assert response.status_code == 200
    assert b"Dep 1" in response.data


def test_department_detail_view_get_wrong_id(module_app, mclient, server):
    response = mclient.get("/departments/42")
    assert response.status_code == 404
    assert b"42 not found" in response.data


def test_create_employee_for_department_post(module_app, mclient, server):
    data = {
        "name": "New Employee",
        "date_of_birth": "1999-05-04",
        "salary": 555,
    }
    response = mclient.post(
        "/departments/1/employees", data=data, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Employee created successfully" in response.data


def test_create_employee_for_department_post_wrong_data(module_app, mclient, server):
    data = {
        "name": "New Employee 2",
        "date_of_birth": "1999-05-04",
        "salary": 0,
    }
    response = mclient.post(
        "/departments/1/employees", data=data, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"This field is required" in response.data


def test_department_edit_view_get(module_app, mclient, server):
    response = mclient.get("/departments/1/edit")
    assert response.status_code == 200


def test_department_edit_view_get_wrong_id(module_app, mclient, server):
    response = mclient.get("/departments/42/edit")
    assert response.status_code == 404
    assert b"id 42 not found" in response.data


def test_department_edit_view_post(module_app, mclient, server):
    data = {"name": "Dep 1 UPD"}
    response = mclient.post("/departments/1/edit", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"updated successfully" in response.data


def test_department_edit_view_post_fails_validation(module_app, mclient, server):
    data = {"name": "D"}
    response = mclient.post("/departments/1/edit", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Field must be between 4 and 50 characters long." in response.data


def test_department_edit_view_post_duplicate_name(module_app, mclient, server):
    data = {"name": "Dep 2"}
    response = mclient.post("/departments/1/edit", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Department names should be unique." in response.data


def test_department_delete_view_get(module_app, mclient, server):
    response = mclient.get("/departments/1/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"Department deleted successfully." in response.data


def test_department_delete_view_get_wrong_id(module_app, mclient, server):
    response = mclient.get("/departments/42/delete")
    assert response.status_code == 404
    assert b"id 42 not found" in response.data
