# pylint: disable=C0301
# pylint: disable=C0116
"""Module contains test for EmployeesAPI and EmployeesSearchAPI classes"""

# Tests for EmployeesAPI

# Tests for GET requests
def test_employees_get_all(client):
    response = client.get("/api/v1/employees")
    assert response.status_code == 200
    assert len(response.json) == 5


def test_employees_get_with_id(client):
    emp_id = 1
    response = client.get(f"/api/v1/employees/{emp_id}")
    assert response.status_code == 200
    assert response.json["id"] == emp_id


def test_employees_get_with_nonexistent_id(client):
    wrong_id = 42
    response = client.get(f"/api/v1/employees/{wrong_id}")
    assert response.status_code == 404
    assert f"id {wrong_id} not found" in response.json["message"]


# Tests for POST requests
def test_employees_post(client):
    data = {
        "name": "New Employee",
        "date_of_birth": "1994-04-05",
        "salary": 777,
        "department_id": 1,
    }
    response = client.post("/api/v1/employees", json=data)
    assert response.status_code == 201
    assert response.json["salary"] == 777


def test_employees_post_wrong_data(client):
    data = {
        "name": "New Employee",
        "date_of_birth": "Not a Date",
        "salary": 777,
        "department_id": 1,
    }
    response = client.post("/api/v1/employees", json=data)
    assert response.status_code == 400


def test_employees_post_nonexistent_department_id(client):
    data = {
        "name": "New Employee",
        "date_of_birth": "1994-04-05",
        "salary": 777,
        "department_id": 42,
    }
    response = client.post("/api/v1/employees", json=data)
    assert response.status_code == 400
    assert response.json["message"] == "Not valid department id"


def test_employees_post_with_id(client):
    emp_id = 1
    data = {
        "name": "New Employee",
        "date_of_birth": "1994-04-05",
        "salary": 777,
        "department_id": 1,
    }
    response = client.post(f"/api/v1/employees/{emp_id}", json=data)
    assert response.status_code == 405


# Tests for PUT requests
def test_employees_put_without_id(client):
    data = {
        "name": "Employee 1 updated",
        "date_of_birth": "1994-04-05",
        "salary": 1001,
        "department_id": 1,
    }
    response = client.put("/api/v1/employees/", json=data)
    assert response.status_code == 405


def test_employees_put_with_id(client):
    emp_id = 1
    data = {
        "name": "Employee 1 updated",
        "date_of_birth": "1994-04-05",
        "salary": 1001,
        "department_id": 1,
    }
    response = client.put(f"/api/v1/employees/{emp_id}", json=data)
    assert response.status_code == 200
    assert response.json["name"] == "Employee 1 updated"


def test_employees_put_with_nonexistent_id(client):
    wrong_id = 42
    data = {
        "name": "Employee 1 updated",
        "date_of_birth": "1994-04-05",
        "salary": 1001,
        "department_id": 1,
    }
    response = client.put(f"/api/v1/employees/{wrong_id}", json=data)
    assert response.status_code == 404
    assert f"id {wrong_id} not found" in response.json["message"]


def test_employees_put_with_id_incomplete_data(client):
    emp_id = 1
    data = {
        "name": "Employee 1 updated",
        "date_of_birth": "1994-04-05",
    }
    response = client.put(f"/api/v1/employees/{emp_id}", json=data)
    assert response.status_code == 400


def test_employees_put_with_id_nonexistent_department_id(client):
    emp_id = 1
    data = {
        "name": "Employee 1 updated",
        "date_of_birth": "1994-04-05",
        "salary": 1001,
        "department_id": 42,
    }
    response = client.put(f"/api/v1/employees/{emp_id}", json=data)
    assert response.status_code == 400
    assert response.json["message"] == "Not valid department id"


# Tests for PATCH requests
def test_employees_patch_without_id(client):
    data = {
        "name": "Employee 1 patch updated",
        "date_of_birth": "2000-04-05",
    }
    response = client.patch("/api/v1/employees", json=data)
    assert response.status_code == 405


def test_employees_patch_with_id(client):
    emp_id = 1
    data = {
        "name": "Employee 1 patch updated",
        "date_of_birth": "2000-04-05",
    }
    response = client.patch(f"/api/v1/employees/{emp_id}", json=data)
    assert response.status_code == 200
    assert response.json["name"] == "Employee 1 patch updated"
    assert response.json["date_of_birth"] == "2000-04-05"


def test_employees_patch_with_nonexistent_id(client):
    wrong_id = 42
    data = {
        "name": "Employee 1 patch updated",
        "date_of_birth": "2000-04-05",
    }
    response = client.patch(f"/api/v1/employees/{wrong_id}", json=data)
    assert response.status_code == 404
    assert f"id {wrong_id} not found" in response.json["message"]


def test_employees_patch_with_id_wrong_data(client):
    emp_id = 1
    data = {
        "name": "Employee 1 patch updated",
        "date_of_birth": "Not a valid date",
    }
    response = client.patch(f"/api/v1/employees/{emp_id}", json=data)
    assert response.status_code == 400


def test_employees_patch_with_id_nonexistent_department_id(client):
    emp_id = 1
    data = {"department_id": 42}
    response = client.put(f"/api/v1/employees/{emp_id}", json=data)
    assert response.status_code == 400


# Tests for DELETE requests
def test_employees_delete_without_id(client):
    response = client.delete("/api/v1/employees")
    assert response.status_code == 405


def test_employees_delete_with_id(client):
    emp_id = 1
    response = client.delete(f"/api/v1/employees/{emp_id}")
    assert response.status_code == 204
    assert len(response.data) == 0


def test_employees_delete_with_nonexistent_id(client):
    wrong_id = 42
    response = client.delete(f"/api/v1/employees/{wrong_id}")
    assert response.status_code == 404
    assert f"id {wrong_id} not found" in response.json["message"]


# Tests for EmployeesSearchAPI

# Tests for searching all employees
def test_employees_search_no_querystring(client):
    response = client.get("/api/v1/employees/search")
    assert response.status_code == 400
    assert response.json["message"] == "Enter search data"


def test_employees_search_one_querystring(client):
    date_to_search = "1991-01-01"
    response = client.get(f"/api/v1/employees/search?date_of_birth={date_to_search}")
    assert response.status_code == 200
    assert all(emp["date_of_birth"] == date_to_search for emp in response.json)


def test_employees_search_two_querystrings(client):
    date_to_search = "1991-01-01"
    date_to_search_2 = "1999-09-09"
    response = client.get(
        f"/api/v1/employees/search?date_of_birth={date_to_search}&date_for_interval={date_to_search_2}"
    )
    assert response.status_code == 200
    assert all(
        date_to_search <= emp["date_of_birth"] <= date_to_search_2
        for emp in response.json
    )


# Tests for searching employees in department


def test_departments_employees_search_no_querystring(client):
    response = client.get("/api/v1/departments/1/employees/search")
    assert response.status_code == 400
    assert response.json["message"] == "Enter search data"


def test_departments_employees_search_one_querystring(client):
    date_to_search = "1991-01-01"
    response = client.get(
        f"/api/v1/departments/1/employees/search?date_of_birth={date_to_search}"
    )
    assert response.status_code == 200
    assert all(emp["date_of_birth"] == date_to_search for emp in response.json)


def test_departments_employees_search_two_querystrings(client):
    dep_id = 1
    date_to_search = "1991-01-01"
    date_to_search_2 = "1999-09-09"
    response = client.get(
        f"/api/v1/departments/{dep_id}/employees/search?date_of_birth={date_to_search}&date_for_interval={date_to_search_2}"
    )
    assert response.status_code == 200
    assert all(
        date_to_search <= emp["date_of_birth"] <= date_to_search_2
        for emp in response.json
    )


def test_departments_employees_search_one_querystring_nonexistent_department(client):
    wrong_dep_id = 42
    date_to_search = "1991-01-01"
    response = client.get(
        f"/api/v1/departments/{wrong_dep_id}/employees/search?date_of_birth={date_to_search}"
    )
    assert response.status_code == 404
    assert f"id {wrong_dep_id} not found" in response.json["message"]
