from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object('app.config.DevelopmentConfig')

cors = CORS(app)
db = SQLAlchemy(app)

from app import views, models

db.create_all()
