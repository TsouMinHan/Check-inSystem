from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO, emit

from config import Config

# =========== app setting ===========
app = Flask(__name__)
app.config.from_object(Config)

socketio = SocketIO(app)

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'main.login'
migrate = Migrate(app, db)
# =========== app setting ===========

from app.view import main as view_bp

app.register_blueprint(view_bp)

from .models import models