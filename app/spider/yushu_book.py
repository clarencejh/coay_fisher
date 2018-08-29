# -*- coding: utf-8 -*-
from app.libs.httper import Http
from flask import current_app


# 查询处理对象
class YuShuBook:
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        # 通过isbn查询
        result = Http.get(self.isbn_url.format(isbn))
        # 将查询到的对象处理一下
        self.__fill_single(result)

    def search_by_keyword(self, keyworld, page=1):
        # 通过 keyword 查询
        result = Http.get(
            self.keyword_url.format(keyworld, current_app.config['PER_PAGE'], self.calculate_start(page)))
        # 将查询到的数据
        self.__fill_collection(result)


    def calculate_start(sele, page):
        return (page - 1) * current_app.config['PER_PAGE']


    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    @property
    def first(self):
        return self.books[0] if self.total>=1 else {}