from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from awarenesscommunity.models import User
from flask_login import current_user


class FormSignup(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    confirmation = PasswordField('Confirm your password', validators=[DataRequired(), EqualTo('password')])
    button_submit_signup = SubmitField('Sign Up')

    def validate_email(self, email):
        usuario = User.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email already registered. Please, use a different email for registration.')

    # def validate_username(self, username):
    #     usuario2 = User.query.filter_by(username=username.data).first()
    #     if usuario2:
    #         raise ValidationError('Username already registered. Please, use a different username for registration.')


class FormSignin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    keep_logged = BooleanField('Keep me signed')
    button_submit_signin = SubmitField('Sign In')


class FormEditProfile(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    class_astro = BooleanField('Astrology')
    class_human_design = BooleanField('Human Desgin')
    class_tarot = BooleanField('Tarot')
    class_pranic = BooleanField('Pranic Healing')
    button_submit_edit_profile = SubmitField('Confirm Edit')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = User.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Email already registered. Please, register a different one.')


class FormPostCreation(FlaskForm):
    title = StringField('Post subject', validators=[DataRequired(), Length(2, 140)])
    body = TextAreaField('Write your post here', validators=[DataRequired()])
    submit_button = SubmitField('Post')
