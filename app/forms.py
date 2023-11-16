from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, SelectField, \
    DateField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class PostForm(FlaskForm):
    title = TextAreaField('Title:', validators=[
        DataRequired(), Length(min=1, max=140)])
    post = TextAreaField('Say something', validators=[
    DataRequired(), Length(min=1, max=140)])
    genretags = SelectMultipleField('genretags', coerce=int, choices=[], validators=[DataRequired()],
                                  render_kw={"multiple": "true"})
    instrtags = SelectMultipleField('instrtags', coerce=int, choices=[], validators=[DataRequired()],
                                    render_kw={"multiple": "true"})
    moodtags = SelectMultipleField('moodtags', coerce=int, choices=[], validators=[DataRequired()],
                                    render_kw={"multiple": "true"})
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    title = TextAreaField('Search')
    genretags = SelectMultipleField('genretags', coerce=int, choices=[], render_kw={"multiple": "true"})
    instrtags = SelectMultipleField('instrtags', coerce=int, choices=[], render_kw={"multiple": "true"})
    moodtags = SelectMultipleField('moodtags', coerce=int, choices=[], render_kw={"multiple": "true"})
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')