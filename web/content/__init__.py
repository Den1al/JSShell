from web.content import routes
from flask import Blueprint

content = Blueprint('content', __name__, url_prefix='/content')
