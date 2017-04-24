from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


def costume_jss_template(config):
    print(config)
    with open('app/static/js/jss_template.js', 'r') as template, \
            open('app/static/js/jss_injected.js', 'w') as injected:

        template_content = template.read().replace('{{ HOST_NAME }}', config['URL'])
        injected.write(template_content)


app = Flask(__name__)
app.config.from_object('app.config.DevelopmentConfig')

cors = CORS(app)

db = SQLAlchemy(app)

from app import views, models

db.create_all()
costume_jss_template(app.config)
