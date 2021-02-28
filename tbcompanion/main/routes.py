import os

from flask import render_template, Blueprint
from tbcompanion import app
from tbcompanion.models import Post, Project

main = Blueprint('main', __name__)

@main.route('/')
def home():
	posts = Post.query.all()
	projects = Project.query.all()
	return render_template('home.html', title='Home', posts=posts, projects=projects)

@main.route('/about')
def about():
	return render_template('about.html', title='About')
