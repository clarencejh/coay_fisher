"""
 Created by 七月 on 2018-2-1.
"""
from flask import jsonify, request, current_app, url_for, render_template, flash
from app.forms.book import SearchForm
import json

from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection
from app.view_models.trade import TradeInfo
from . import web


@web.route('/book/search')
def search():
    """
        q :普通关键字 isbn
        page
        ?q=金庸&page=1
    """

    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = yushu_book.first

    # TradeInfo 将查询到的数据传入viewmodel 调整数据结构
    trade_gifts = TradeInfo(Gift.query.filter_by(isbn=isbn, launched=False).all())
    trade_wishes = TradeInfo(Wish.query.filter_by(isbn=isbn, launched=False).all())

    return render_template('book_detail.html', book=book, wishes=trade_wishes, gifts=trade_gifts)
