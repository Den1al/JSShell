from flask import render_template
from web.main import main


@main.route('/', methods=['GET'])
def index():
    """ The view that holds the main page.
        JSShell will be injected to that page, so
        any testing / running can be done using this page.
        """

    return render_template('index.html')


@main.route('/favicon.ico', methods=['GET'])
def favicon():
    """ I got tired of seeing 404 for the `favicon.ico`,
        so I created this route ... """

    return b'\x41\x41\x41\x41'
