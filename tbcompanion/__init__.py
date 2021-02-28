from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from tbcompanion.config import Config

app = Flask(__name__)
app.config.from_object(Config)


mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_man = LoginManager(app)

login_man.login_view = 'users.login'
login_man.login_message_category = 'info'


from tbcompanion.accounts.routes import accounts
from tbcompanion.admin.routes import admin
from tbcompanion.main.routes import main
from tbcompanion.posts.routes import posts
from tbcompanion.projects.routes import projects
from tbcompanion.users.routes import users

app.register_blueprint(accounts)
app.register_blueprint(admin)
app.register_blueprint(main)
app.register_blueprint(posts)
app.register_blueprint(projects)
app.register_blueprint(users)