"""This module contains class-based forms generated using wtf-forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, NumberRange


class DepartmentForm(FlaskForm):
    """
    Class creates form for accepting user data for department adding/editing.
    Provides data validation.
    """

    name = StringField(
        "",
        validators=[DataRequired(), Length(4, 50)],
        render_kw={"placeholder": "Department Name"},
    )
    submit = SubmitField("Save department")


class EmployeeForm(FlaskForm):
    """
    Class creates form for accepting user data for employee adding/editing.
    Provides data validation.
    """

    def __init__(self, departments, *args, **kwargs):
        """
        Initiate an EmployeeForm instance, accepts a positional argument 'departments'
        based on which generates the list of existing departments for select field.
        """
        super().__init__(*args, **kwargs)
        self.department_id.choices = [(dep["id"], dep["name"]) for dep in departments]

    name = StringField(
        "",
        validators=[DataRequired(), Length(4, 100)],
        render_kw={"placeholder": "Employee Name"},
    )
    date_of_birth = DateField("", validators=[DataRequired()])
    salary = IntegerField(
        "",
        validators=[DataRequired(), NumberRange(1)],
        render_kw={"placeholder": "Salary"},
    )
    department_id = SelectField(
        "",
        validators=[DataRequired()],
    )
    submit = SubmitField("Save employee")
