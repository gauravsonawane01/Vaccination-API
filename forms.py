from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    fname = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AppointmentForm(FlaskForm):

    phoneNumber = StringField('Phone Number',
                           validators=[DataRequired(), Length(max=10)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    age = StringField('Age',
                       validators=[DataRequired(), Length(max=2)])
    date = StringField('Date',
                              validators=[DataRequired(), Length(max=10)])
    city = StringField('City',
                           validators=[DataRequired(), Length(min=2, max=20)])
    state = StringField('State',
                           validators=[DataRequired(), Length(min=2, max=20)])
    zip = StringField('Zip',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit')
