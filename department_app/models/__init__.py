"""
Module contains classes thad define database models,
based on Flask-SQLAlchemy db.Model
"""
from department_app import db


class Department(db.Model):
    """This class defines a database table for departments"""

    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    employees = db.relationship(
        "Employee", cascade="all,delete", backref=db.backref("department")
    )