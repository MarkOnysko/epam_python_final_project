[![Build Status](https://travis-ci.com/MarkOnysko/epam_python_final_project.svg?branch=master)](https://travis-ci.com/MarkOnysko/epam_python_final_project)
[![Coverage Status](https://coveralls.io/repos/github/MarkOnysko/epam_python_final_project/badge.svg?branch=master)](https://coveralls.io/github/MarkOnysko/epam_python_final_project?branch=master)

# Department App

## Description

A simple web application for managing departments and employees. Uses REST-API
for CRUD operations. Allows to:

- display all departments, and the average salary for these departments.
- display all employees with their information(name, date of birth, salary,
  department).
- display employees in a particular department.
- search employees born on a specified date or in an interval between dates,
  both among all employees and employees of a particular department.
- add, update and delete departments and employees.

## Prerequisites

In order to run application with docker you"ll need Docker and Docker Compose installed.

* [Docker installation info](https://docs.docker.com/get-docker/)
* [Docker Compose installation info](https://docs.docker.com/compose/install/)

## Usage

Build
-----

### Steps to build the app with docker(it will use a PostrgreSQL database):

1. Clone this repo:

        git clone https://github.com/MarkOnysko/epam_python_final_project.git

2. Proceed to the epam_python_final_project directory:
 
        cd epam_python_final_project

3. Compose the docker containers:

        docker-compose up

    This will take a few minutes.


4. Once everything has started up, you should be able to access the app with test data added at
   [http://0.0.0.0:5000/](http://0.0.0.0:5000/) on your host machine.
   
### Steps to build the app without docker(it will use an SQLite database):

1. Clone this repo:

        git clone https://github.com/MarkOnysko/epam_python_final_project.git

2. Proceed to the epam_python_final_project directory:
 
        cd epam_python_final_project

3. Run the "install_and_run.sh" script:
      
       ./install_and_run.sh

4. Once everything has started up, you should be able to access the app with test data added at
   [http://127.0.0.1:5000/](http://0.0.0.0:5000/) on your host machine.
   
## API endpoints

* "/api/v1/departments"
    * GET - get all departments.
    * POST - create new department. Data:
      ```json 
      {"name": <str>}
      ```
    
* "/api/v1/departments/<dep_id>"
    * GET - get department by id. Returns json with department id, department name,
      list of employees and average salary.
    * PUT - update department. Data:
      ```json 
      {"name": <str>}
      ```
    * PATCH - update department. Data:
      ```json 
      {"name": <str>}
      ```
    * DELETE - delete department with all its employees.
  

* "/api/v1/departments/<dep_id>/employees"
    * GET - get all employees in specified department.
    * POST - create a new employee in specified department. Data(all fields required):
      ```json
      {"name": <str>, "birthday": "%Y-%m-%d" <str>, "salary": <int>}
      ```
      

* "/api/employees"
    * GET - get all employees
    * POST - create a new employee. Data (every field required):
      ```json
      {"name": <str>, "birthday": <"%Y-%m-%d" str>, "salary": <int>, "dep_name": <str>}
      ```
      
* "/api/employees/<emp_id>"
    * GET - get employee by id.
    * PUT - update employee. Data (all fields required):
      ```json 
      {"name": <str>, "birthday": <"%Y-%m-%d" str>, "salary": <int>, "dep_id": <int>}
      ```
    * PATCH - update employee. Data (any field):
      ```json 
      {"name": <str>, "birthday": <"%Y-%m-%d" str>, "salary": <int>, "dep_id": <int>}
      ```
    * DELETE - delete employee by id  
  

* "/api/v1//employees/search"
    * GET - search for employees born on a specified date or in an
      interval among all employees. Data:
      
       * query parameters: ?date_of_birth=<%Y-%m-%d>&[date_for_interval=<%Y-%m-%d>]


* "/api/v1/departments/<dep_id>/employees/search""
    * GET - search for employees born on a specified date or in an
      interval among all employees of the specified department. Data:
      
      * query parameters: ?date_of_birth=<%Y-%m-%d>&[date_for_interval=<%Y-%m-%d>]