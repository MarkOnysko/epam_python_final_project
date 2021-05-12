# pylint: disable=E1101
"""Module contains a function to populate test data in DB."""
from datetime import date
from department_app import create_app
from department_app.models import Department, Employee, db


def populate_db():
    """Populates DB with data, used during tests."""
    d_1 = Department(name="Dep 1")
    d_2 = Department(name="Dep 2")

    e_1 = Employee(
        name="Employee 1",
        date_of_birth=date(year=1991, month=1, day=1),
        salary=1000,
        department_id=1,
    )

    e_2 = Employee(
        name="Employee 2",
        date_of_birth=date(year=1992, month=2, day=2),
        salary=1000,
        department_id=1,
    )

    e_3 = Employee(
        name="Employee 3",
        date_of_birth=date(year=1993, month=3, day=3),
        salary=2000,
        department_id=2,
    )

    e_4 = Employee(
        name="Employee 4",
        date_of_birth=date(year=1994, month=4, day=4),
        salary=2000,
        department_id=2,
    )

    e_5 = Employee(
        name="Employee 5",
        date_of_birth=date(year=1995, month=5, day=5),
        salary=2000,
        department_id=2,
    )

    db.session.add(d_1)
    db.session.add(d_2)
    db.session.add(e_1)
    db.session.add(e_2)
    db.session.add(e_3)
    db.session.add(e_4)
    db.session.add(e_5)
    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        populate_db()
