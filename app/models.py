from app import db
import datetime


def _get_date():
    return datetime.datetime.now()


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key = True)
    client_id = db.Column(db.String(36), unique = True)
    user_agent = db.Column(db.String(1024))
    ip = db.Column(db.String(15))
    last_beaconed = db.Column(db.DateTime(), default=_get_date)
    commands = db.relationship('Command', back_populates="client")

    def get_printable(self):
        for cmd in self.commands:
            if cmd.is_returned and not cmd.is_printed:
                return cmd

    def update_beacon(self):
        self.last_beaconed = _get_date()


    def add_command(self, cmd):
        c = Command(cmd)
        self.commands.append(c)
        db.session.add(c)

    def add_commands(self, cmds):
        for cmd in cmds:
            self.add_command(cmd)

    def __init__(self, uuid, user_agent, ip):
        self.client_id = uuid
        self.user_agent = user_agent
        self.ip = ip

    def __repr__(self):

        c = ''
        for com in self.commands:
            c += repr(com).lstrip()

        s = '''
<client>
    <id>{}</id>
    <uuid>{}</uuid>
    <user_agent>{}</user_agent>
    <ip_address>{}</ip_address>
    <commands>
        {}
    </command>
</client>
'''.format(self.id, self.client_id, self.user_agent, self.ip, c.rstrip() or 'no commands')

        return s[1:-1]



class Command(db.Model):
    __tablename__ = 'command'
    id = db.Column(db.Integer, primary_key=True)
    cmd = db.Column(db.String(1024))
    output = db.Column(db.String(1024))
    created_on = db.Column(db.DateTime(), default=_get_date)
    is_served = db.Column(db.Boolean, default=0)
    is_returned = db.Column(db.Boolean, default=0)
    is_printed = db.Column(db.Boolean, default=0)
    rel_client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship("Client", back_populates="commands")

    def __init__(self, cmd, output = ''):
        self.cmd = cmd
        self.output = output

    def __repr__(self):
        return '''
        <command>
            <id>{}</id>
            <cmd>{}</cmd>
            <output>{}</output>
            <created_on>{}</created_on>
            <is_served>{}</is_served>
            <is_returned>{}</is_returned>
            <is_printed>{}</is_printed>
            <rel_client>{}<rel_client>
        </command>
        '''.format(self.id, self.cmd, self.output, self.created_on, self.is_served, self.is_returned, self.is_printed, self.rel_client_id)[1:-1]



