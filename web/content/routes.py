from flask import render_template, url_for, Response

from common.config import read_config
from common.utils import concat_url_path
from web.content import content


@content.route('/jquery', methods=['GET'])
def get_jquery():
    """ Returns the jQuery.js file """

    return render_template('javascript/jquery.js')


@content.route('/prune', methods=['GET'])
def get_prune():
    """ Returns the prune.js file """

    return render_template('javascript/prune.js')


@content.route('/js', methods=['GET'])
def get_javascript():
    """ The view that returns the actual javascript shell
        to the client. It takes in consideration configuration
        from the `config.json` file. It also appends the dependencies
        which are `jQuery` and `JSON.prune`. """

    config = read_config()
    url = config.get('URL', '//')

    shell_javascript = render_template(
        'javascript/shell.js',
        post_back_url=concat_url_path(url, url_for('api.post_back')),
        poll_url=concat_url_path(url, url_for('api.poll_new_commands')),
        register_url=concat_url_path(url, url_for('api.register'))
    )

    script_content = '\n\n'.join([
        render_template('javascript/jquery.js'),
        'var JJ = $.noConflict(true);',
        render_template('javascript/prune.js'),
        shell_javascript
    ])

    return Response(script_content, mimetype='application/javascript')
