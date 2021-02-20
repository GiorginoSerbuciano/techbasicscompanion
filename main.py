from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
db = SQLAlchemy(app)

@app.route('/')
def home():
	return 'Hello World!'

app.run()

class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True, nullable=False)

	def __repr__(self):
		return '<User %r>' % self.username


admin = User(username='Administrator', email='admin@email.com')
user01 = User(username='User01', email='user01@email.com')

db.create_all()
db.session.add(admin)
db.session.add(user01)
db.session.commit()

print(User.query.filter_by(username='Administrator').first())