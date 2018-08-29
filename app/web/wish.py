from flask import current_app, flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from app import db
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from . import web

__author__ = '七月'


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gitf_count_list = Wish.get_gift_counts(isbn_list)
    gitf_ViewModel = MyTrades(wishes_of_mine, gitf_count_list)
    return render_template('my_wish.html', wishes=gitf_ViewModel.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        # 自定时的事务提交
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']   # 0.5
            db.session.add(wish)

    else:
        flash("这本书已添加到你的赠送清单或索要书单!")
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
