from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
import sqlite_code

class RegistrationForm(FlaskForm):
  username = StringField('Username',
                         validators=[DataRequired(),
                                     Length(min=5, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
  confirm_password = PasswordField(
    'Confirm Password', validators=[DataRequired(),
                                    EqualTo('password')])
  submit = SubmitField('Sign Up')

  def validate_username(self, username):
      if sqlite_code.user_lookup(username.data):
        raise ValidationError('Username taken. Please choose another one.')
  
  def validate_email(self, email):
      if sqlite_code.email_lookup(email.data):
        raise ValidationError('Email taken. Please choose another one.')


class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

class PostForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired()])
  content = TextAreaField('Content', validators=[DataRequired()])
  submit = SubmitField('Post')
