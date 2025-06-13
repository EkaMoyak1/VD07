from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

from wtforms.validators import Regexp


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(message="Обязательное поле"),
        Length(min=4, max=25, message="Длина должна быть от 4 до 25 символов"),
        Regexp(r'^[A-Za-z][A-Za-z0-9_.]*$',
               message="Разрешены только буквы, цифры, точки и подчёркивания. Должно начинаться с буквы")
    ])

    email = StringField('Email', validators=[
        DataRequired(message="Обязательное поле"),
        Email(message="Некорректный email")
    ])

    password = PasswordField('Пароль', validators=[
        DataRequired(message="Обязательное поле"),
        Length(min=8, message="Пароль должен содержать минимум 8 символов"),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$',
               message="Пароль должен содержать заглавные, строчные буквы и цифры")
    ])

    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(message="Обязательное поле"),
        EqualTo('password', message="Пароли должны совпадать")
    ])

    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован. Пожалуйста, используйте другой email.')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[
        DataRequired(message="Введите логин")
    ], render_kw={"autocomplete": "username"})  # Указываем autocomplete

    password = PasswordField('Пароль', validators=[
        DataRequired(message="Введите пароль")
    ], render_kw={"autocomplete": "current-password"})

    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                          validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

# В forms.py
from wtforms.validators import DataRequired, Length, Regexp

password = PasswordField('Password', validators=[
    DataRequired(),
    Length(min=8),
    Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$',
           message="Пароль должен содержать цифры, заглавные и строчные буквы")
])