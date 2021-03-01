from flask import render_template, Blueprint
from tbcompanion.models import Post, Project
from sqlalchemy import desc

main = Blueprint('main', __name__)

@main.route('/')
def home():
	posts = Post.query.order_by(desc('date')).all()
	projects = Project.query.order_by(desc('date')).all()
	return render_template('home.html', title='Home', posts=posts, projects=projects)

@main.route('/about')
def about():
	return render_template('about.html', title='About')

#TODO: Complete 'about'