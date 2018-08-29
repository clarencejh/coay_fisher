# -*- coding: utf-8 -*-
# app.__init__


from flask import Flask
from . import setting, secure
from app.models import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()

def create_app():
    # 实例app
    app = Flask(__name__)
    # 添加config
    app.config.from_object(setting)
    app.config.from_object(secure)
    # 注册蓝图
    register_blueprint(app)
    # 连接mysql
    db.init_app(app)
    db.create_all(app=app)
    # 注册登录模块
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    mail.init_app(app)
    return app

def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)