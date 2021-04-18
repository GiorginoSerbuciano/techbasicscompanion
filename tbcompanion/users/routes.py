from flask import Blueprint, render_template, request, url_for
from flask.helpers import flash
from flask_login import login_user, logout_user
from flask_login.utils import login_required
from werkzeug.utils import redirect

from tbcompanion import bcrypt
from tbcompanion.models import Post, User
from tbcompanion.users.forms import LoginForm

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
	"""This is the page where registered users can log in."""

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			after_login_page = request.args.get('next')  # Allows returning users to the page they were on previously.
			flash(f'Welcome back, {user.username}!', 'success')
			return redirect(after_login_page) if after_login_page else redirect(url_for('main.home'))
		else:
			flash('Login unsuccessful. :(', 'danger')

	return render_template('login.html', title='Login', form=form)


@users.route('/logout', methods=['GET'])
def logout():
	"""Logout route."""
	logout_user()
	flash('You are logged out. See ya\'!', 'info')
	return redirect(url_for('main.home'))


@users.route('/users')
@login_required
def search_users():
	"""Displays a list of all registered users."""
	user_search = User.query.all()
	return render_template('user_search.html', 
		users=user_search,
		title='Users')


@users.route('/users/<int:user_id>')
@login_required
def user_profile(user_id):
	"""This page displays the profile of a different registered user to the current user."""

	user = User.query.get_or_404(user_id)
	posts = Post.query.filter_by(author=user)
	projects = user.contribution_id

	return render_template('user_profile.html', 
		user=user, 
		posts=posts, 
		projects=projects,
		title=user.username)
