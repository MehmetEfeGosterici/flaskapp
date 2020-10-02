from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, email_validator, ValidationError
from flaskapp.models import User

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[ DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=20)])
    confirm = PasswordField("confirm Password", validators=[EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(Username = username.data ).first()
        if user:
            raise ValidationError("this Username already exists. Please choose another one")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data ).first()
        if user:
            raise ValidationError("this Username already exists. Please choose another one")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[ DataRequired(), Email() ])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign up")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[ DataRequired(), Email()])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
         if username.data != current_user.Username:
            user = User.query.filter_by(Username = username.data ).first()
            if user:
                raise ValidationError("this Username already exists. Please choose another one")

    def validate_email(self, email):
         if email.data != current_user.email:   
            user = User.query.filter_by(email = email.data ).first()
            if user:
                raise ValidationError("this Username already exists. Please choose another one")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")