from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Length


class Register(FlaskForm):
    username = StringField("username", validators=[InputRequired()])
    # email = StringField('email', validators=[Email(), InputRequired()])
    password = PasswordField(
        "Password",
        validators=[
            Length(min=2, max=50),
            InputRequired(),
            EqualTo("confirm", message="Passwords must match."),
        ],
    )
    confirm = PasswordField("Repeat password", validators=[InputRequired()])
    accept_tos = BooleanField(
        'I accept the <a href="#tos">Terms of Service</a> and the <a href="#priv"> Privacy Policy</a>',
        validators=[InputRequired()],
    )
    submit = SubmitField(
        "Register", render_kw={"class": "btn waves-effect waves-light white-text"}
    )


class Login(FlaskForm):
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("New Password", validators=[InputRequired()])
    submit = SubmitField(
        "Login", render_kw={"class": "btn waves-effect waves-light white-text"}
    )
