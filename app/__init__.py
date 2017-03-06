from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object('app.config.DevelopmentConfig')

db = SQLAlchemy(app)

from app import views, models
