# -*- coding: utf-8 -*-
from sqlalchemy.orm import relationship

from app.models import db, Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger, func, desc

from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)

    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))

    isbn = Column(String(15), nullable=False)

    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))

    # 获取第一本书的对象
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first


    # 获取用户 赠送的所有 想要的礼物
    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        from app.models.gift import Gift

        # 根据传入的一组isbn 到gift表中计算某个礼物的gift心愿数量

        # 一组数量 使用 func.count 根据isbn分组 计算 id数量

        # 根据isbn_list 使用 in_查询
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list)
        ).group_by(Gift.isbn).all()
        # 元组形式
        # [(1, '9780596515829'), (1, '9787020002207'), (1, '9787121068744')]
        # 应该返回字典 或者 对象
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list


