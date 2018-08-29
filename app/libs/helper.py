# -*- coding: utf-8 -*-

def is_isbn_or_key(word):
    """isbn
    13
    个0 - 9
    的数字组成
    也有
    10
    个数字组成的, 中间包含
    '-'
    字符
"""
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_q = word.replace('-', '')
    if '-' in word and len(short_q) == 10 and short_q.isdigit():
        isbn_or_key = 'isbn'

    return isbn_or_key