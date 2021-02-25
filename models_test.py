from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from tbcompanion import app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///:memory:'
db = SQLAlchemy(app)

class User(db.Model):
	
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable = False)
	email = db.Column(db.String(120), unique=True, nullable = False)
	image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	is_admin = db.Column(db.Boolean, nullable=False)

	def __repr__(self):
		return "User('{}','{}','{}','{}')".format(
			self.username,self.email, self.image_file, self.is_admin)

db.create_all()
test_user = User(username='dev', email='dev@email.com', password='dev', is_admin=True)
db.session.add(test_user)
db.session.commit()
print(User.query.all())