from app import db
from app.models.gift import Gift
from app.view_models.trade import MyTrades
from . import web
from flask_login import login_required, current_user
from flask import current_app, flash, redirect, url_for, render_template

__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    # 用户礼物 isbn列表
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    count_list = Gift.get_wish_counts(isbn_list)
    my_gifts_ViewModel= MyTrades(gifts_of_mine, count_list)
    return render_template('my_gifts.html', gifts=my_gifts_ViewModel.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # 自定时的事务提交
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']   # 0.5
            db.session.add(gift)

    else:
        flash("这本书已添加到你的赠送清单或索要书单!")
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass


