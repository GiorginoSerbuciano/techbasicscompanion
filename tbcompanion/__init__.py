from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from tbcompanion.config import Config


mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_man = LoginManager()


login_man.login_view = 'users.login'
login_man.login_message_category = 'info'



def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	mail.init_app(app)
	db.init_app(app)
	bcrypt.init_app(app)
	login_man.init_app(app)

	from tbcompanion.accounts.routes import accounts
	from tbcompanion.admin.routes import admin
	from tbcompanion.main.routes import main
	from tbcompanion.posts.routes import posts
	from tbcompanion.projects.routes import projects
	from tbcompanion.users.routes import users
	from tbcompanion.errors.handlers import errors
	app.register_blueprint(accounts)
	app.register_blueprint(admin)
	app.register_blueprint(main)
	app.register_blueprint(posts)
	app.register_blueprint(projects)
	app.register_blueprint(users)
	app.register_blueprint(errors)

	return app