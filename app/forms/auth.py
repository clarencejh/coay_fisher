# -*- coding: utf-8 -*-

from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError, EqualTo

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])

    password1 = PasswordField(validators=[DataRequired(message='密码不可以为空!'), Length(6, 32, message='密码长度为6到32位'), EqualTo('password2', message='两次密码一样')])
    password2 = PasswordField(validators=[DataRequired(message='密码不可以为空!'), Length(6, 32, message='密码长度为6到32位')])

    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少需要两个字符, 最多十个字符')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('改邮件已注册')


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])

    password = PasswordField(validators=[DataRequired(message='密码不可以为空!'), Length(6, 32, message='密码长度为6到32位')])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])


class ResetPassword(Form):
    password1 = PasswordField(validators=[
        DataRequired(message='密码不可以为空!'),
        Length(6, 32, message='密码长度为6到32位'),
        EqualTo('password2', message='两次密码一样')])

    password2 = PasswordField(validators=[
        DataRequired(), Length(6, 32)
    ])
