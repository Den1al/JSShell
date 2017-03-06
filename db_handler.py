from app import app, db
from app.models import Client, Command
import argparse
import uuid

def sqltry(func):
    def wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print('Error occurred:', e)
            return None
    return wrap


@sqltry
def createTable():
    print('Creating table...')
    db.create_all()
    print('Done!')


@sqltry
def listRecords():
    print('Listing records...')
    clients = Client.query.all()

    for c in clients:
        print(c)


@sqltry
def insertRecord(_idDefault = str(uuid.uuid4()), userAgentDefault = 'Mozilla Testing/1.0', ipDefault = '127.0.0.1'):
    print('Enter Values: ')

    _id = input('UUID: ')
    if not _id: _id = _idDefault

    user_agent = input('User-Agent: ')
    if not user_agent: user_agent = userAgentDefault

    ip = input('IP: ')
    if not ip: ip = ipDefault

    c = Client(_id, user_agent, ip)
    db.session.add(c)
    db.session.commit()


@sqltry
def insertDummy():
    _id = str(uuid.uuid4())
    user_agent = 'Mozilla Testing/1.0'
    ip = '127.0.0.1'
    c = Client(_id, user_agent, ip)
    db.session.add(c)
    db.session.commit()


@sqltry
def dropTable():
    if input('Sure? [y/n]') == 'y':
        db.drop_all()
        print('Table dropped.')
    else:
        print('Bad choice. Bye!')

@sqltry
def dropCreateList():
    dropTable()
    createTable()
    listRecords()


@sqltry
def truncateTable():
    Client.query.delete()
    db.session.commit()


@sqltry
def createCommand():
    i = input('Enter Client ID: ')
    c = Command('aaa','bbb')
    u = Client.query.filter_by(id=int(i)).first()
    u.commands.append(c)
    db.session.add(c)
    db.session.commit()


if __name__ == "__main__":

    actions = {
        'list' : listRecords,
        'create' : createTable,
        'insert' : insertRecord,
        'dummy' : insertDummy,
        'drop' : dropTable,
        'dcl' : dropCreateList,
        'trunc' : truncateTable,
        'com' : createCommand
    }

    parser = argparse.ArgumentParser(description='DB Handler')
    parser.add_argument('action', choices=actions.keys())



    args = parser.parse_args()
    actions[args.action]()
