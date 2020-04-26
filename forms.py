from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import InputRequired, EqualTo, Email

class Register(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    #email = StringField('email', validators=[Email(), InputRequired()])
    password = PasswordField(
        'Password',
        [
            validators.Length(min=2),
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat password')
    submit = SubmitField('Register', render_kw={'class': 'btn waves-effect waves-light white-text'})

class Login(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn waves-effect waves-light white-text'})