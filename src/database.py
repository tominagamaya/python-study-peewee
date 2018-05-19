import functools

from peewee import *

db = SqliteDatabase('my_app.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()


class Message(BaseModel):
    user = ForeignKeyField(User, backref='messages')
    content = TextField()


def test_database():
    db.create_tables([User, Message])
    with db.transaction() as tx:
        piyo = User.create(username='piyo', password='ppp', email='piyo@com')
        tx.commit()

        huga = User.create(username='huga', password='hhh', email='huga@com')
        tom = User.create(username='tom', password='ttt', email='tom@com')

        print "======= start ========="
        for user in User.select():
            print user.username

        tx.rollback()
        print "======= rollback ========="
        for user in User.select():
            print user.username


def mock_transaction(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with db.transaction() as tx:
            try:
                print "======= start ========="
                func(*args, **kwargs)
            except:
                print "======= error ========="
            finally:
                print "======= finish ========="
                tx.rollback()

    return wrapper


@mock_transaction
def test_mock():
    db.create_tables([User])
    piyo = User.create(username='piyo', password='ppp', email='piyo@com')
    huga = User.create(username='huga', password='hhh', email='huga@com')
    tom = User.create(username='tom', password='ttt', email='tom@com')

    for user in User.select():
        print user.username


if __name__ == '__main__':
    test_mock()
    try:
        for user in User.select():
            print user.username
    except:
        print "No User Table!"
