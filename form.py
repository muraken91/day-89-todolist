from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired


# WTForm for creating a new task
class TodoForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    priority = SelectField('Priority', validators=[DataRequired()],
                                choices=["Low", "Medium", "High"])
    status = SelectField('Status', validators=[DataRequired()],
                                choices=["Not Started", "In Progress", "Completed"])
    type = SelectField('Task Type', validators=[DataRequired()],
                                choices=["Python", "Javascript", "Work", "Daily"])
    submit = SubmitField('Submit')

