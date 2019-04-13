from web.api import api as api_bp
from web.content import content as content_bp
from web.main import main as main_bp
from flask import Flask
from flask_cors import CORS

from common.config import read_config
from common.models import db


config = read_config()
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = config.get('MONGO', {})
CORS(app)

db.init_app(app)

app.register_blueprint(api_bp)

app.register_blueprint(content_bp)

app.register_blueprint(main_bp)


def start_api_server() -> None:
    """ Starts the web server """

    app.run(
        host=config.get('HOST', 'localhost'),
        port=config.get('PORT', 5000),
        debug=config.get('DEBUG', False)
    )
