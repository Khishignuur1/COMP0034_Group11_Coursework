"""
    Based on https://github.com/UCLComputerScience/comp0034_flask_login_complete and
    https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog
    Adapted by 17075800
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User


# Creates a Signup form
class SignupForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email(message='Valid email address required')])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

    # Validates the username's uniqueness (queries the database for entered username and presents error if match found)
    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose a different one.')
            
    # Validates the email's uniqueness (queries the database for entered email and presents error if match found)
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')

            
# Creates a Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')


# Creates an account update form
class UpdateAccountForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email(message='Valid email address required')])
    submit = SubmitField('Update')
    
    # Validates the username's uniqueness (queries the database for entered username and presents error if match found)
    def validate_name(self, name):
        if name.data != current_user.name:
            user = User.query.filter_by(name=name.data).first()
            if user:
                raise ValidationError('This username is taken. Please choose a different one.')
    
    # Validates the email's uniqueness (queries the database for entered email and presents error if match found)
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is taken. Please choose a different one.')

# Creates an Item form
class ItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    price = IntegerField('Price /£', validators=[DataRequired()])
    color = SelectField('Color', choices=[('black', 'Black'), ('white', 'White'), ('red', 'Red'), ('orange', 'Orange'),
                                          ('yellow', 'Yellow'), ('green', 'Green'), ('blue', 'Blue'), ('pink', 'Pink')])
    size = SelectField('Size', choices=[('xxs', 'XXS'), ('xs', 'XS'), ('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL'),
                                        ('xxl', 'XXL')])
    submit = SubmitField('Create')
