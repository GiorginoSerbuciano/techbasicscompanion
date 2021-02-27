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
	return render_template('post_view.html', title=post.title, post=post)


@app.route('/project/<int:project_id>', methods=['GET'])
def project(project_id):
	project = Project.query.get_or_404(project_id)
	return render_template('project_view.html', title=project.title, project=project)


@app.route('/logout', methods=['GET'])
def logout():
	logout_user()
	flash('You are logged out. See ya\'!', 'info')
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
	if form.validate_on_submit():
		print('Form validated!')
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('You have updated your account.', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('account.html', title=current_user.username,
		user=current_user, form=form, posts=posts, projects=projects)


@app.route('/project/new', methods=['GET', 'POST'])
@login_required
def project_form():
	form = ProjectForm()
	tags = Tag.query.order_by(Tag.id).all()
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
	return render_template('project_form.html', form=form, type='project', tags=tags)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def post_form():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('You have published your post!', 'success')
		return redirect(url_for('home'))
	return render_template('post_form.html', form=form, title='New Post')

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	print(post.id)
	if post.author != current_user:
		print(current_user)
		abort(403)
	form = PostForm()
	print('Entering validation conditional...')
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('You have updated your post!', 'success')
		print('Form validated!')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
		print('elif conditional: Filled in form fields!')
	return render_template('post_form.html', form=form, title='New Post')

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		print(current_user)
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('You have deleted your post!', 'danger')
	return redirect(url_for('home'))


def send_password_reset_email(user):
	token = user.get_reset_token()
	msg = Message(
		'TBCOMP::password_reset',
		sender='serban.gorga@gmail.com',
		recipients=[user.email])
	msg.body=f"""If you reqested a password reset, click this link to reset your password:
{url_for('password_reset', token=token, _external=True)}

TBCOMP@DEV_GiorginoSerbuciano
	"""
	mail.send(msg)

@app.route('/passwordReset', methods=['GET','POST'])
def password_reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = ForgotPassword()
	if form.validate_on_submit():
		user =  User.query.filter_by(email=form.email.data).first()
		send_password_reset_email(user)
		flash('If this email corresponds to a registered account, you will shortly receive an email with a link to reset your password.', 'info')
		print('Reset email sent to',user.email)
		return redirect(url_for('login'))
	return render_template('password_reset_request.html', title='Reset Password', form=form)



@app.route('/passwordReset/<token>', methods=['POST'])
def password_reset(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	user = User.validate_reset_token(token)
	if not user:
		flash('Invalid token!', 'warning')
		return redirect(url_for('password_reset_request'))
	form = PasswordReset()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pass
		flash('You\'ve set a new password!', 'success')
		return redirect(url_for('login'))	
	return render_template('password_reset.html', title='Set a new password', form=form)

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
	return render_template('admin.html')