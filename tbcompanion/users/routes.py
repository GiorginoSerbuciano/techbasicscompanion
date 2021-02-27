from flask import Blueprint, render_template, request, url_for
from flask.helpers import flash
from flask_login import login_user, logout_user
from flask_login.utils import login_required
from tbcompanion import bcrypt
from tbcompanion.forms import LoginForm
from tbcompanion.models import Post, Project, User
from werkzeug.utils import redirect

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
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


@users.route('/logout', methods=['GET'])
def logout():
	logout_user()
	flash('You are logged out. See ya\'!', 'info')
	return redirect(url_for('home'))

@users.route('/users')
@login_required
def users():
	users = User.query.all()
	return render_template('user_search.html', users=users)


@users.route('/users/<int:user_id>')
@login_required
def user_profile(user_id):
	user = User.query.get_or_404(user_id)
	posts = Post.query.filter_by(author=user)
	projects = Project.query.filter_by(contributor=user)
	return render_template('user_profile.html', user=user, posts=posts, projects=projects)
