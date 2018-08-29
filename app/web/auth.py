from app import db
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPassword
from app.models.user import User
from . import web
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.libs.email import send_mail

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # 自定义事务提交
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            user.password = form.password1.data
            db.session.add(user)

        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if not next or next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        form = EmailForm(request.form)
        if form.validate():
            accont_emaile = form.email.data
            user = User.query.filter_by(email=accont_emaile).first_or_404()
            send_mail(accont_emaile, '重置密码', 'email/reset_password.html', user=user, token=user.generate_token())
            flash(f'已向 {accont_emaile} 发送邮件, 请查收.')
            return redirect(url_for('web.index'))
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPassword(request.form)
    if request.method == 'POST' and form.validate():
        successs = User.resetpassword(token, form.password1.data)
        if successs:
            flash('已成功修改密码, 请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败, 请重试')
    return render_template('auth/forget_password.html')


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
