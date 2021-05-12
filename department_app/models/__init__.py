"""
Module contains classes thad define database models,
based on Flask-SQLAlchemy db.Model
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Department(db.Model):
    """This class defines a database table for departments"""

    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    employees = db.relationship(
        "Employee", cascade="all,delete", backref=db.backref("department")
    )


class Employee(db.Model):
    """This class defines a database table for employees"""

    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False, index=True)
    salary = db.Column(db.Integer, nullable=False)
    department_id = db.Column(
        db.Integer, db.ForeignKey("departments.id"), nullable=False
    )
