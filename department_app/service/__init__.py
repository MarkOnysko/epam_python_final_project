""""Module contains Service classes with methods for DB CRUD operations."""
from department_app.models import Department, Employee, db


class DepartmentServices:
    """Class with methods for DB CRUD operation on departments."""

    @staticmethod
    def get_all():
        """
        This method returns a list with all Department objects from the DB.
        Or an empty list if no department entries in DB.
        """
        return Department.query.all()

    @staticmethod
    def get_by_id(dep_id):
        """
        Get a specific department by id from DB.
        :param dep_id: Id of the department to fetch (int)
        :return: Department with id=dep_id, None if no such department.
        """
        return Department.query.filter_by(id=dep_id).first()

    @staticmethod
    def create(data):
        """
        Create a new Department instance from dict and save new entry to DB
        :param data: A dict with data to create a department from.
        :return: the created instance
        """
        department = Department(**data)
        db.session.add(department)
        db.session.commit()
        return department

    @staticmethod
    def update(department, data):
        """
        Update a Department object and related DB entry with data from dict.
        :param department: A Department instance.
        :param data: A dict with data to update the department with.
        :return: The updated instance.
        """
        for key in data:
            if key in department.__dict__.keys():
                department.__setattr__(key, data[key])
        db.session.commit()
        return department

    @staticmethod
    def delete(department):
        """
        Delete a Department instance and related data from DB
        :param department: The department to be deleted.
        :return: None
        """
        db.session.delete(department)
        db.session.commit()

    @staticmethod
    def get_avg_salary(department):
        """
        Calculate the average salary for employees in working department.
        :param department: A Department instance to calculate the average for.
        :return: The average salary round to 2 digits after point.
                 0 if no employees in the department.
        """
        if not department.employees:
            return 0
        return round(
            sum([employee.salary for employee in department.employees])
            / len(department.employees),
            2,
        )


class EmployeeServices:
    """Class with methods for DB CRUD operation on departments."""

    @staticmethod
    def get_all():
        """
        This method returns a list with all Employee objects from the DB.
        Or an empty list if no employees in DB.
        """
        return Employee.query.all()

    @staticmethod
    def get_all_for_department(dep_id):
        """
        Get all employees working in a specified departmentю
        :param dep_id: ID of the department(int)
        :return: A list with all Employee instances with "department_id=dep_id"
        Or an empty list if no employees in department with id=dep_id.
        """
        return Employee.query.filter_by(department_id=dep_id).all()

    @staticmethod
    def get_by_date_of_birth(date, date_for_interval=None):
        """
        Get employees born on a specific date or in an interval between dates.
        :param date: date object to get employees born on specific date
        or lower point for interval to get employees born in interval
        (if date_for_interval passed).
        :param date_for_interval: date object to specify the upper point
        for interval to get employees born in interval.
        :return: a list of employees with date_of_birth matching the provided
        parameters. Empty list if no matches.
        """
        if not date_for_interval:
            return Employee.query.filter_by(date_of_birth=date).all()
        return Employee.query.filter(
            Employee.date_of_birth.between(date, date_for_interval)
        ).all()

    @staticmethod
    def get_by_date_of_birth_from_department(dep_id, date, date_for_interval=None):
        """
        Get employees born on a specific date or in an interval between dates,
        who work in a specified department.
        :param dep_id: Id of the department to get employees from (int).
        :param date: date object to get employees born on specific date
        or lower point for interval to get employees born in interval
        (if date_for_interval passed).
        :param date_for_interval: date object to specify the upper point
        for interval to get employees born in interval.
        :return: a list of employees with date_of_birth matching the provided
        parameters. Empty list if no matches.
        """
        if not date_for_interval:
            return (
                Employee.query.filter_by(date_of_birth=date)
                    .filter_by(department_id=dep_id)
                    .all()
            )
        return (
            Employee.query.filter(
                Employee.date_of_birth.between(date, date_for_interval)
            )
                .filter_by(department_id=dep_id)
                .all()
        )

    @staticmethod
    def get_by_id(emp_id):
        """
        Get a specific employee by id from DB.
        :param emp_id: Id of the employee to fetch (int)
        :return: Employee with id=dep_id, None if no such department.
        """
        return Employee.query.filter_by(id=emp_id).first()

    @staticmethod
    def create(data):
        """
        Create a new Employee instance from dict and save new entry to DB
        :param data: A dict with data to create an employee from.
        :return: the created instance
        """
        db.session.execute("pragma foreign_keys=on")
        employee = Employee(**data)
        db.session.add(employee)
        db.session.commit()
        return employee

    @staticmethod
    def update(employee, data):
        """
        Update an Employee object and related DB entry with data from dict.
        :param employee: An Employee instance to be updated.
        :param data: A dict with data to update the employee with.
        :return: The updated instance.
        """
        db.session.execute("pragma foreign_keys=on")
        for key in data:
            if key in employee.__dict__.keys():
                employee.__setattr__(key, data[key])
        db.session.commit()
        return employee

    @staticmethod
    def delete(employee):
        """
        Delete an Employee instance and related data from DB
        :param employee: The employee to be deleted.
        :return: None
        """
        db.session.delete(employee)
        db.session.commit()
