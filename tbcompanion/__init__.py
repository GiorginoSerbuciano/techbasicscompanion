from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from flaskext.markdown import Markdown
from tbcompanion.config import Config

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_man = LoginManager()
pd = PageDown()

login_man.login_view = 'users.login'
login_man.login_message_category = 'info'


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	mail.init_app(app)
	db.init_app(app)
	bcrypt.init_app(app)
	login_man.init_app(app)
	pd.init_app(app)
	md = Markdown(app)

	from tbcompanion.accounts.routes import accounts
	app.register_blueprint(accounts)

	from tbcompanion.admin.routes import admin
	app.register_blueprint(admin)

	from tbcompanion.main.routes import main
	app.register_blueprint(main)

	from tbcompanion.posts.routes import posts
	app.register_blueprint(posts)

	from tbcompanion.projects.routes import projects
	app.register_blueprint(projects)

	from tbcompanion.users.routes import users
	app.register_blueprint(users)

	from tbcompanion.errors.handlers import errors
	app.register_blueprint(errors)

	return app
