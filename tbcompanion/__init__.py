from flask import Flask
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_man = LoginManager(app)
login_man.login_view = 'login'
login_man.login_message_category = 'info'

# helo plis message for tedi: you are the cutest tedi in the universe and i love youuuuuuuu!!!!!!!!!

from tbcompanion import routes
