# manage.py
# from dotenv import load_dotenv
# load_dotenv()
# import unittest
# import coverage
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from src import create_app, db
from src.models import *

import logging

app = create_app()

manager = Manager(app)
migrate = Migrate(app,db)

# migrations
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='127.0.0.1', port='5000')
    logging.info('Flask app run')

@manager.command
def recreate_db():
    # Recreate a local db
    db.drop_all()
    db.create_all()
    db.session.commit()
    logging.warning("DB was recreated.")

# @manager.command
# def test():
#     tests = unittest.TestLoader().discover('api/tests', pattern='test*.py')
#     result = unittest.TextTestRunner(verbosity=2).run(tests)
#     if result.wasSuccessful():
#         return 0
#     return 1
if __name__ == '__main__':
    manager.run()
