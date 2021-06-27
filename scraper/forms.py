from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import phonenumbers
from scraper.models import User, Ticker


class RegistrationForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already exists. Please choose a different one.')

    def validate_phone(self, phone):
        parsed_phone = phonenumbers.parse(phone.data, 'US')
        if not phonenumbers.is_valid_number(parsed_phone):
            raise ValidationError('Invalid phone number. Try retyping without symbols.')

class LoginForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    photo = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username already exists. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email already exists. Please choose a different one.')

    def validate_phone(self, phone):
        parsed_phone = phonenumbers.parse(phone.data, 'US')
        if not phonenumbers.is_valid_number(parsed_phone):
            raise ValidationError('Invalid phone number. Try retyping without symbols.')

class AddTicker(FlaskForm):

    ticker = StringField('Ticker', validators=[DataRequired(), Length(min=3, max=5)])
    submit = SubmitField('Add')

    def validate_ticker(self, ticker):
        db_ticker = Ticker.query.filter_by(ticker_id=ticker.data.upper()).first()
        if db_ticker is None:
            raise ValidationError('Ticker is invalid or cannot be found. Please choose a different one.')
