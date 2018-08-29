# -*- coding: utf-8 -*-
from flask import current_app
from sqlalchemy.orm import relationship

from app.models import db, Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger, desc, func

from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)

    # 关联用户id
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    # 图书 isbn
    isbn = Column(String(15), nullable=False)
    
    # 交易时 判断是否是自己的书
    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    # 获取第一本书的对象
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 对象代表一个礼物, 具体的礼物
    # 类代表礼物这一类, 他是抽象的, 不是具体的 某一个
    @classmethod
    def recent(cls):
        # 最近上传

        # 链式调用
        # 主体 Query
        # 子函数 每个子函数都会返回主体->Query
        # 触发语句 all() first()
        recent_gift = Gift.query.filter_by(  # 查询条件
            launched=False).group_by(  # 去重条件
            Gift.isbn).order_by(  # 排序条件
            desc(Gift.create_time)).limit(  # 查询条数
            current_app.config['RECENT_BOOK_COUNT']).all()  # 触发语句
        return recent_gift

    # 获取用户 赠送的所有礼物
    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        # 根据传入的一组isbn 到wish表中计算某个礼物的wish心愿数量

        # 一组数量 使用 func.count 根据isbn分组 计算 id数量

        # 根据isbn_list 使用 in_查询
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list)
        ).group_by(Wish.isbn).all()
        # 元组形式
        # [(1, '9780596515829'), (1, '9787020002207'), (1, '9787121068744')]
        # 应该返回字典 或者 对象
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list


