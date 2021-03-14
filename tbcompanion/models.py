from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from tbcompanion import db, login_man



@login_man.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	is_admin = db.Column(db.Boolean)
	post_author = db.relationship('Post', backref='author', lazy=True)
	project_admin = db.relationship('Project', backref='admin', lazy=True)
	project_contributor = db.relationship('Project', backref='contributor', lazy=True)

	def __repr__(self):
		return "User('{}','{}','{}')".format(
			self.username, self.email, self.image_file, self.post_author)

	def get_reset_token(self, expires_sec=900):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def validate_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

	def __repr__(self):
		return "Post('{}','{}','{}')".format(
			self.title, self.date, self.user_id)


class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	github_repo = db.Column(db.String(120), nullable=True, unique=True)
	admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	tag = db.Column(db.String, nullable=True)

	def __repr__(self):
		return "Project('{}','{}','{}')".format(
			self.title, self.date)

