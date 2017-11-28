from app import app, db
from app.models import Client, Command
import argparse
import uuid

def sqltry(func):
    """ A Decorator that quietly runs a command """
    def wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print('Error occurred:', e)
            return None
    return wrap


@sqltry
def create_table():
    """ Creates the table """
    print('Creating table...')
    db.create_all()
    print('Done!')


@sqltry
def list_records():
    """ Lists all records """
    print('Listing records...')
    clients = Client.query.all()

    for c in clients:
        print(c)


def list_client():
    """ Lists a specific client """
    client_id = int(input('Which client to list?>> '))
    c = Client.query.filter_by(id=client_id).first()

    if not c:
        print('Client does not exists.')
        return

    print(c)

@sqltry
def insert_record(_id_default = str(uuid.uuid4()), ua_default ='Mozilla Testing/1.0', ip_default ='127.0.0.1'):
    """ Inserts a records to the DB """
    print('Enter Values: ')

    _id = input('UUID: ')
    if not _id: _id = _id_default

    user_agent = input('User-Agent: ')
    if not user_agent: user_agent = ua_default

    ip = input('IP: ')
    if not ip: ip = ip_default

    c = Client(_id, user_agent, ip)
    db.session.add(c)
    db.session.commit()


@sqltry
def insert_dummy():
    """ Inserts a dummy object to the DB """
    _id = str(uuid.uuid4())
    user_agent = 'Mozilla Testing/1.0'
    ip = '127.0.0.1'
    c = Client(_id, user_agent, ip)
    db.session.add(c)
    db.session.commit()


@sqltry
def drop_table():
    """ Drops the table """
    if input('Sure? [y/n]') == 'y':
        db.drop_all()
        print('Table dropped.')
    else:
        print('Bad choice. Bye!')

@sqltry
def drop_create_list():
    """ Drops -> Creates -> Lists the database """
    drop_table()
    create_table()
    list_records()


@sqltry
def truncate_table():
    """ Truncates the database """
    Client.query.delete()
    db.session.commit()


@sqltry
def create_command():
    """ Creates a command """

    i = input('Enter Client ID: ')
    c = Command('aaa','bbb')
    u = Client.query.filter_by(id=int(i)).first()
    u.commands.append(c)
    db.session.add(c)
    db.session.commit()


if __name__ == "__main__":

    actions = {
        'list': list_records,
        'client': list_client,
        'create': create_table,
        'insert': insert_record,
        'dummy': insert_dummy,
        'drop': drop_table,
        'dcl': drop_create_list,
        'trunc': truncate_table,
        'com': create_command
    }

    parser = argparse.ArgumentParser(description='DB Handler')
    parser.add_argument('action', choices=actions.keys())

    args = parser.parse_args()
    actions[args.action]()
