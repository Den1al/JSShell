from web.api import routes
from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')
