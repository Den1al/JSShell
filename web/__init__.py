from flask import Flask
from flask_cors import CORS
# from OpenSSL import SSL

from common.config import read_config
from common.models import db

config = read_config()
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = config.get('MONGO', {})
CORS(app)

db.init_app(app)

from web.api import api as api_bp
app.register_blueprint(api_bp)

from web.content import content as content_bp
app.register_blueprint(content_bp)

from web.main import main as main_bp
app.register_blueprint(main_bp)


def start_api_server() -> None:
    """ Starts the web server """

    domain_name = config.get('DOMAIN', '')
    lets_encrypt_base_path = f'/etc/letsencrypt/live/{domain_name}/'

    # ssl_context = SSL.Context(SSL.TLSv1_2_METHOD)
    # ssl_context.use_privatekey_file(lets_encrypt_base_path + 'privkey.pem')
    # ssl_context.use_certificate_chain_file(lets_encrypt_base_path + 'fullchain.pem')
    # ssl_context.use_certificate_file(lets_encrypt_base_path + 'cert.pem')

    app.run(
        host=config.get('HOST', 'localhost'),
        port=config.get('PORT', 5000),
        debug=config.get('DEBUG', False),
        ssl_context=(
            lets_encrypt_base_path + 'cert.pem',
            lets_encrypt_base_path + 'privkey.pem'
        )
    )
