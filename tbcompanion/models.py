from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tbcompanion import db, login_man
from flask_login import UserMixin

@login_man.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable = False)
	email = db.Column(db.String(120), unique=True, nullable = False)
	image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)
	projects = db.relationship('Project', backref='contributor', lazy=True)
	#backref: like adding a new column using Post.author;
	#lazy: can return all posts by the same author
	def __repr__(self):
		return "User('{}','{}','{}')".format(
			self.username,self.email, self.image_file, self.posts)


class Post(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable = False)
	date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	#id of the user; 'user' is not the object, but the table name!
	def __repr__(self):
		return "Post('{}','{}','{}')".format(
			self.title,self.date,self.user_id)


class Project(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable = False)
	date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable = False)
	github_repo = db.Column(db.String(120), nullable = False, unique = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	#id of the user; 'user' is not the object, but the table name!
	def __repr__(self):
		return "Project('{}','{}','{}')".format(
			self.title,self.date,self.user_id)


db.create_all()