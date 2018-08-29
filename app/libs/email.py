# -*- coding: utf-8 -*-
from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_async_email(app, msg):
    try:
        mail.send(msg)
    except Exception:
        pass


def send_mail(to, subject, template, **kwargs):
    # msg = Message('测试邮件', sender='jhcj.z@qq.com', body='Test', recipients=['clarencepy@163.com'])
    msg = Message('[今后从简]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                   recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

    # mail.send(msg)