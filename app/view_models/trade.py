# -*- coding: utf-8 -*-

# 书籍详情页面 下方已赠送书单
from collections import namedtuple

from app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return dict(
            user_name = single.user.nickname,
            time = time,
            id=single.id
        )


MyWish = namedtuple('MyWish', ['id', 'book', 'wishes_count'])


class MyTrades:
    def __init__(self, trades_of_mine, wish_count_list):
        self.trades = []

        self.__trades_of_mine = trades_of_mine
        self.__wish_count_list = wish_count_list

        self.trades = self.__parse()
        pass

    def __parse(self):
        temp_trades = []
        for gift in self.__trades_of_mine:
            my_gift = self.__matching(gift)
            temp_trades.append(my_gift)
        return temp_trades

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        my_gift = MyWish(gift.id, BookViewModel(gift.book), count)
        return my_gift