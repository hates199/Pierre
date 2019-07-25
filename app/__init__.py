from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # Object that will represent the database
migrate = Migrate(app, db) # Migration Object

from app import routes