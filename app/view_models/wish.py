# -*- coding: utf-8 -*-
from collections import namedtuple

from app.view_models.book import BookViewModel

MyWish = namedtuple('MyWish', ['id', 'book', 'wishes_count'])


class MyWishes:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.wishes = []

        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list

        self.wishes = self.__parse()
        pass

    def __parse(self):
        temp_gifts = []
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        my_gift = MyWish(gift.id, BookViewModel(gift.book), count)
        return my_gift

#
# class MyGift:
#     def __init__(self):
#         pass