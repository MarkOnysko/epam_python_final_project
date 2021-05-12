# pylint: disable=C0116
"""Module contains test for DepartmentAPI and DepartmentEmployeesAPI classes"""


# Tests for DepartmentAPI

# Tests for GET requests
def test_departments_get_all(client):
    response = client.get("/api/v1/departments")
    assert response.status_code == 200
    assert len(response.json) == 2


def test_departments_get_with_id(client):
    response = client.get("/api/v1/departments/1")
    assert response.status_code == 200
    assert response.json["name"] == "Dep 1"


def test_departments_get_with_nonexistent_id(client):
    wrong_id = 42
    response = client.get(f"/api/v1/departments/{wrong_id}")
    assert response.status_code == 404
    assert f"id {wrong_id} not found" in response.json["message"]


# Tests for POST requests
def test_departments_post(client):
    data = {"name": "Dep 3"}
    response = client.post("/api/v1/departments", json=data)
    assert response.status_code == 201
    assert response.json["name"] == "Dep 3"


def test_departments_post_wrong_data(client):
    data = {"title": "Dep 3"}
    response = client.post("/api/v1/departments", json=data)
    assert response.status_code == 400


def test_departments_post_duplicate_name(client):
    data = {"name": "Dep 2"}
    response = client.post("/api/v1/departments", json=data)
    assert response.status_code == 400
    assert "Department names should be unique." in response.json["message"]


def test_departments_post_with_id(client):
    data = {"name": "Dep 3"}
    response = client.post("/api/v1/departments/1", json=data)
    assert response.status_code == 405


# Tests for PUT requests
def test_departments_put_without_id(client):
    data = {"name": "Dep 3"}
    response = client.put("/api/v1/departments/", json=data)
    assert response.status_code == 405


def test_departments_put_with_id(client):
    data = {"name": "Dep Updated"}
    response = client.put("/api/v1/departments/1", json=data)
    assert response.status_code == 200
    assert response.json["name"] == "Dep Updated"


def test_departments_put_with_nonexistent_id(client):
    wrong_id = 42
    data = {"name": "Dep Updated"}
    response = client.put(f"/api/v1/departments/{wrong_id}", json=data)
    assert response.status_code == 404
    assert f"id {wrong_id} not found" in response.json["message"]


def test_departments_put_with_id_wrong_data(client):
    data = {"title": "Dep 3"}
    response = client.put("/api/v1/departments/1", json=data)
    assert response.status_code == 400


def test_departments_put_with_id_duplicate_name(client):
    data = {"name": "Dep 2"}
    response = client.put("/api/v1/departments/1", json=data)
    assert response.status_code == 400
    assert "Department names should be unique." in response.json["message"]


# Tests for PATCH requests
def test_departments_patch_without_id(client):
    data = {"name": "Dep 3"}
    response = client.patch("/api/v1/departments/", json=data)
    assert response.status_code == 405


def test_departments_patch_with_id(client):
    data = {"name": "Dep Updated"}
    response = client.patch("/api/v1/departments/1", json=data)
    assert response.status_code == 200
    assert response.json["name"] == "Dep Updated"


def test_departments_patch_with_nonexistent_id(client):
    wrong_id = 42
    data = {"name": "Dep Updated"}
    response = client.patch(f"/api/v1/departments/{wrong_id}", json=data)
    assert response.status_code == 404
    assert f"id {wrong_id} not found" in response.json["message"]


def test_departments_patch_with_id_wrong_data(client):
    data = {"title": "Dep 3"}
    response = client.patch("/api/v1/departments/1", json=data)
    assert response.status_code == 400


def test_departments_patch_with_id_duplicate_name(client):
    data = {"name": "Dep 2"}
    response = client.patch("/api/v1/departments/1", json=data)
    assert response.status_code == 400
    assert "Department names should be unique." in response.json["message"]


# Tests for DELETE requests
def test_departments_delete_without_id(client):
    response = client.delete("/api/v1/departments")
    assert response.status_code == 405


def test_departments_delete_with_id(client):
    response = client.delete("/api/v1/departments/1")
    assert response.status_code == 204
    assert len(response.data) == 0


def test_departments_delete_with_nonexistent_id(client):
    wrong_id = 42
    response = client.delete(f"/api/v1/departments/{wrong_id}")
    assert response.status_code == 404
    assert f"id {wrong_id} not found" in response.json["message"]


# Tests for DepartmentEmployeesAPI

# Tests for GET requests
def test_departments_employees_get_without_id(client):
    response = client.get("/api/v1/departments/employees")
    assert response.status_code == 404


def test_departments_employees_get_with_id(client):
    dep_id = 1
    response = client.get(f"/api/v1/departments/{dep_id}/employees")
    assert response.status_code == 200
    assert all(emp["department"]["id"] == dep_id for emp in response.json)


def test_departments_employees_get_with_nonexistent_id(client):
    wrong_id = 42
    response = client.get(f"/api/v1/departments/{wrong_id}/employees")
    assert response.status_code == 404
    assert f"id {wrong_id} not found" in response.json["message"]


# Tests for POST requests
def test_departments_employees_post_without_id(client):
    data = {
        "name": "New Employee",
        "date_of_birth": "1999-01-01",
        "salary": 5000,
    }
    response = client.post("/api/v1/departments/employees", json=data)
    assert response.status_code == 405


def test_departments_employees_post_with_id(client):
    dep_id = 1
    data = {
        "name": "New Employee",
        "date_of_birth": "1995-05-05",
        "salary": 5000,
    }
    response = client.post(f"/api/v1/departments/{dep_id}/employees", json=data)
    assert response.status_code == 201
    assert response.json["department"]["id"] == dep_id
    assert response.json["name"] == "New Employee"


def test_departments_employees_post_with_nonexistent_id(client):
    wrong_id = 42
    data = {
        "name": "New Employee",
        "date_of_birth": "1995-05-05",
        "salary": 5000,
    }
    response = client.post(f"/api/v1/departments/{wrong_id}/employees", json=data)
    assert response.status_code == 404
    assert f"id {wrong_id} not found" in response.json["message"]


def test_departments_employees_post_with_id_wrong_data(client):
    dep_id = 1
    data = {
        "name": "New Employee",
        "date_of_birth": "1995-05-05",
        "salary": -5000,
    }
    response = client.post(f"/api/v1/departments/{dep_id}/employees", json=data)
    assert response.status_code == 400


# Tests for not allowed request methods
def test_departments_employees_put(client):
    dep_id = 1
    data = {
        "name": "New Employee updated",
        "date_of_birth": "1995-05-05",
        "salary": 7777,
    }
    response = client.put(f"/api/v1/departments/{dep_id}/employees", json=data)
    assert response.status_code == 405


def test_departments_employees_patch(client):
    dep_id = 1
    data = {
        "name": "New Employee patched update",
    }
    response = client.patch(f"/api/v1/departments/{dep_id}/employees", json=data)
    assert response.status_code == 405


def test_departments_employees_delete(client):
    dep_id = 1
    response = client.delete(f"/api/v1/departments/{dep_id}/employees")
    assert response.status_code == 405
