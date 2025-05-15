from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class RegisterationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=2,max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password') ,Length(min=2,max=60)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=2,max=20)])
    remember = BooleanField('Remember Me: ')
    submit = SubmitField('Sign In')
    
class RatingsForm(FlaskForm):
    #title = StringField('Title', validators=[DataRequired()])
    title = StringField('Title',validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired(), NumberRange(min=0.0, max=5.0,message="Please give a rating between 0 and 5")])
    #FloatField('Rating', validators=[DataRequired(), NumberRange(min=0.0,max=5.0,message="Please give a rating between 0 and 5")])
    submit = SubmitField('Rate')