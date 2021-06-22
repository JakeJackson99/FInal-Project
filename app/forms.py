"""The forms used in the program.

There are two forms used in the program: the login form for the admin users and
the data form for those partaking in the experiment.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """A form for loggin in.

    Args:
        FlaskForm: Inherates from Flask-WTF.
    """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class DataForm(FlaskForm):
    """A form for collecting provided information on users.

    Args:
        FlaskForm: Inherates from Flask-WTF.
    """

    age = IntegerField('Age', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    submit = SubmitField('Submit')