from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jinja2

app = Flask(__name__)
app.config.from_object('app.config.DevelopmentConfig')

my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['app/static/js/',
                                 'app/templates/']),
    ])

app.jinja_loader = my_loader

cors = CORS(app)
db = SQLAlchemy(app)

from app import views, models

db.create_all()
