from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length


class RegisterForm(FlaskForm):
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    email = StringField('email', validators=[InputRequired(),
                                             Email(message='正しいメールアドレスを入力して下さい'), Length(max=255)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=255)])
    submit = SubmitField('submit')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=5)])
    password = PasswordField('パスワード', validators=[InputRequired(), Length(min=8, max=255)])
    remember = BooleanField('remember me')
    submit = SubmitField('submit')
