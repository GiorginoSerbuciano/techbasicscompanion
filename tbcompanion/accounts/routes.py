from flask import Blueprint, render_template, request, url_for
from flask.helpers import flash
from flask_login import current_user
from flask_login.utils import login_required
from flask_mail import Message
from tbcompanion import bcrypt, db, mail
from tbcompanion.accounts.forms import (ForgotPassword, PasswordReset,
										RegistrationForm, UpdateAccount)
from tbcompanion.models import Post, User
from werkzeug.utils import redirect

accounts = Blueprint('accounts', __name__)


@accounts.route('/register', methods=['GET', 'POST'])
def register():
	"""This is the page where new users can register."""

	if current_user.is_authenticated:  # User must not be logged in. Redirect to registration page if False.
		flash('You are already registered!')
		return redirect(url_for('main.home'))

	form = RegistrationForm()

	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data,
					email=form.email.data,
					password=hashed_pass)

		db.session.add(user)
		db.session.commit()

		flash(f'Welcome, {form.username.data}!', 'success')
		return redirect(url_for('main.home'))

	return render_template('register.html', title='Register', form=form)

# TODO: E-mail confirmation


@accounts.route('/account', methods=['GET', 'POST'])
@login_required
def account_page():
	"""This is the page where registered, logged-in users can see their own profile and update their account info."""

	posts = Post.query.filter_by(author=current_user).all()
	projects = current_user.contribution_id

	form = UpdateAccount()

	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data

		db.session.commit()  # User already exists, just need to commit new data.

		flash('You have updated your account.', 'success')
		return redirect(url_for('accounts.account_page'))

	elif request.method == 'GET':  # Fills form fields with the user's information.
		form.username.data = current_user.username
		form.email.data = current_user.email

	return render_template('account.html',
						   title=current_user.username,
						   user=current_user,
						   form=form,
						   posts=posts,
						   projects=projects)


# TODO: Expand UpdateAccount.

def send_password_reset_email(user):
	"""Uses flask_mail to sends users an email with a link to reset their password."""

	token = user.get_reset_token()  # Carries over to .password_reset
	msg = Message(  # flask_mail.Message
		'TBCOMP::password_reset',
		sender='serban.gorga@gmail.com',
		recipients=[user.email])
	msg.body = ("If you requested a password reset, click this link to reset your password:\n"
				f"{url_for('accounts.password_reset', token=token, _external=True)}\n"  # Redirects to .password_reset
				"TBCOMP@DEV_GiorginoSerbuciano")
	mail.send(msg)  # flask_mail._MailMixin.send


@accounts.route('/passwordReset', methods=['GET', 'POST'])
def password_reset_request():
	"""Allows users to request an email with a password reset link to be sent to their email address."""

	if current_user.is_authenticated:  # User must not be logged in.
		return redirect(url_for('main.home'))

	form = ForgotPassword()  # Asks for user email.

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_password_reset_email(user)

		flash('If this email corresponds to a registered account,'
			  'you will shortly receive an email with a link to reset your password.',
			  'info')  # This vague formulation does not reveal whether an account exists under the given email.
		return redirect(url_for('users.login'))

	return render_template('password_reset_request.html',
						   title='Reset Password',
						   form=form)


@accounts.route('/passwordReset/<token>', methods=['GET','POST'])
def password_reset(token):
	"""Password reset link redirects to this page. Resets user's password. """

	if current_user.is_authenticated:  # User must not be logged in.
		return redirect(url_for('main.home'))

	user = User.validate_reset_token(token)  # See .send_password_reset_email

	if not user:  # Checks if the current token is (still) valid.
		flash('Invalid token!', 'warning')
		return redirect(url_for('accounts.password_reset_request'))

	form = PasswordReset()

	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pass
		# db.session.commit()?

		flash('You\'ve set a new password!', 'success')
		return redirect(url_for('users.login'))

	return render_template('password_reset.html',
						   title='Set a new password',
						   form=form)
