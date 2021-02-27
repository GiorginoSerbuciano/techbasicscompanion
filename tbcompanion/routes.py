import os
from flask import Flask, render_template, url_for, request
from flask.helpers import flash
from flask_login import login_user, current_user, logout_user
from flask_login.utils import login_required
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from tbcompanion import app, db, bcrypt, mail
from tbcompanion.models import User, Post, Project, Tag
from tbcompanion.forms import ProjectForm, RegistrationForm, LoginForm, UpdateAccount, PostForm, PasswordReset, ForgotPassword
from flask_mail import Message

app.config['SECRET_KEY'] = os.environ.get('SECRETKEY')

### PUBLIC PAGES ###

@app.route('/')
def home():
	posts = Post.query.all()
	projects = Project.query.all()
	return render_template('home.html', title='Home', posts=posts, projects=projects)

@app.route('/about')
def about():
	return render_template('about.html', title='About')























