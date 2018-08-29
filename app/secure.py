# -*- coding: utf-8 -*-


DIALECT = 'mysql'
DRIVER = 'cymysql'
USENAME = 'root'
PASSWORD = 'root'
dbHOST = '127.0.0.1'
PORT = 3306
DATABASE = 'fisher'

SQLALCHEMY_DATABASE_URI = f'{DIALECT}+{DRIVER}://{USENAME}:{PASSWORD}@{dbHOST}:{PORT}/{DATABASE}?charset=utf8'

SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = b'\xb1g\xb8\xeb\xf1\\\xa4jW\xd1"\tZ\xf3y{\x1ai6\xb92\xb6\xc2\t'


MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = ''      # 邮箱
MAIL_PASSWORD = ''      # 邮箱授权码


