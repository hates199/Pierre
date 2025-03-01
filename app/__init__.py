from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # Object that will represent the database
migrate = Migrate(app, db) # Migration Object
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models