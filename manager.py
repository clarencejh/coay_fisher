# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.models import db

manager = Manager(create_app)

migrate = Migrate(create_app, db)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
