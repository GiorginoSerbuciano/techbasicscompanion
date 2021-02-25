from flask import Flask, render_template, url_for, request
from flask.helpers import flash
from flask_login import login_user, current_user, logout_user
from flask_login.utils import login_required
from werkzeug.utils import redirect
from tbcompanion import app, db, bcrypt
from tbcompanion.models import User, Post, Project
from tbcompanion.forms import ProjectForm, RegistrationForm, LoginForm, UpdateAccount, PostForm

app.config['SECRET_KEY'] = 'ba61fd67ee8ec9771cff83f85d5289c4'


### PUBLIC PAGES ###

@app.route('/')
def home():
	posts = Post.query.all()
	projects = Project.query.all()
	return render_template('home.html', title='Home', posts=posts, projects=projects)


@app.route('/about')
def about():
	return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		flash('You are already registered!')
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
		db.session.add(user)
		db.session.commit()
		flash(f'Welcome, {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			after_login_page = request.args.get('next')
			flash(f'Welcome back, {user.username}!', 'success')
			return redirect(after_login_page) if after_login_page else redirect(url_for('home'))
		else:
			flash('Login unsuccessful. :(', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route('/post/<int:post_id>', methods=['GET'])
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)


@app.route('/project/<int:project_id>', methods=['GET'])
def project(project_id):
	project = Project.query.get_or_404(project_id)
	return render_template('project_view.html', title=project.title, project=project)


@app.route('/logout', methods=['GET'])
def logout():
	logout_user()
	flash('You have been logged out. See ya\'!', 'info')
	return redirect(url_for('home'))


### PAGES WITH LOGIN REQUIRED ###

@app.route('/users')
@login_required
def users():
	users = User.query.all()
	return render_template('user_search.html', users=users)


@app.route('/users/<int:user_id>')
@login_required
def user_profile(user_id):
	user = User.query.get_or_404(user_id)
	posts = Post.query.filter_by(author=user)
	projects = Project.query.filter_by(contributor=user)
	return render_template('user_profile.html', user=user, posts=posts, projects=projects)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	posts = Post.query.filter_by(author=current_user)
	projects = Project.query.filter_by(contributor=current_user)
	form = UpdateAccount()
	return render_template('account.html', title=current_user.username, user=current_user, form=form, posts=posts, projects=projects)


@app.route('/project/new', methods=['GET', 'POST'])
@login_required
def project_form():
	form = ProjectForm()
	if form.validate_on_submit():
		project = Project(
			title=form.title.data,
			content=form.content.data,
			contributor=current_user,
			github_repo=form.github_repo.data)
		db.session.add(project)
		db.session.commit()
		flash('Your project is live!', 'success')
		return redirect(url_for('home'))
	return render_template('project_form.html', form=form, type='project')


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def post_form():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been published!', 'success')
		return redirect(url_for('home'))
	return render_template('post_form.html', form=form, title='New Post')
