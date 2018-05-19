from database import User
from peewee import *

db = SqliteDatabase('my_app.db')


class TestDatabase:
    def __init__(self):
        pass

    def test_select(self):
        a = User.create(username='piyo', password='ppp', email='piyo@com')

    def test_find(self):
        with db.transaction() as tx:
            # setup
            User.create(username='piyo', password='ppp', email='piyo@com')
            # execute
            data = User.select()
            # cleanup
            tx.rollback()

        # verify
        assert len(data) == 1


def test_find():
    pass


if __name__ == '__main__':
    TestDatabase.test_find()
