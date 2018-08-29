# -*- coding: utf-8 -*-
from math import floor

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as tmSerializer

from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models import db, Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from app.models.dirft import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True, )
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String(128), nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)

    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)

    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)
    
    # 登录时验证密码   generate_password_hash 和 check_password_hash 
    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not  yushu_book.first:
            return False

        # 不允许一个用户同时赠送多本相同的图书
        # 一个用户不能同时成为赠送者和索要者
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()

        # 这本书既不在赠送清单也不再索要清单才能添加
        if not gifting and not wishing:
            return True
        else:
            return False

    # 解析获得的 token  然后重置密码
    @staticmethod
    def resetpassword(token, new_password):
        s = tmSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    # 验证邮箱
    @staticmethod
    def Verifying_mailbox(token):
        s = tmSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            # 验证参数
            user.confirmed = True
        return True

    # 生产产生url的 token
    def generate_token(self, expriation=600):
        s = tmSerializer(current_app.config['SECRET_KEY'], expriation)
        temp = s.dumps({'id': self.id}).decode('utf-8')
        return temp

    # 是否可以发送鱼漂
    def can_send_drift(self):
        if self.beans < 1:
            return False

        success_gifts_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.success).count()
        return True if floor(success_receive_count/2) <= floor(success_gifts_count) else False

    # 简介
    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter)+'/'+str(self.receive_counter)
        )


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
