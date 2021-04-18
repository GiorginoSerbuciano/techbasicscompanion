from flask import Blueprint, render_template, request, url_for
from flask.helpers import flash
from flask_login import current_user
from flask_login.utils import login_required
from flask_mail import Message
from tbcompanion import bcrypt, db, mail
from tbcompanion.accounts.forms import (ForgotPassword, PasswordReset,
										RegistrationForm, UpdateAccount)
from tbcompanion.models import Post, Project, User
from werkzeug.utils import redirect

accounts = Blueprint('accounts', __name__)


### REGISTRATION ###
@accounts.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		flash('You are already registered!')
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
		db.session.add(user)
		db.session.commit()
		flash(f'Welcome, {form.username.data}! You will shortly receive an activation email.', 'success')
		return redirect(url_for('main.home'))
	return render_template('register.html', title='Register', form=form)


# TODO: E-mail confirmation

# ACCOUNT PAGE & DETAILS UPDATE
@accounts.route('/account', methods=['GET', 'POST'])
@login_required
def account_page():
	posts = Post.query.filter_by(author=current_user).all()
	projects = current_user.contribution_id
	form = UpdateAccount()
	if form.validate_on_submit():
		print('Form validated!')
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('You have updated your account.', 'success')
		return redirect(url_for('accounts.account_page'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('account.html',
						   title=current_user.username,
						   user=current_user,
						   form=form,
						   posts=posts,
						   projects=projects)


# BEGIN PASSWORD RESET

def send_password_reset_email(user):
	token = user.get_reset_token()
	msg = Message(
		'TBCOMP::password_reset',
		sender='serban.gorga@gmail.com',
		recipients=[user.email])
	msg.body = f"""If you reqested a password reset, click this link to reset your password:
{url_for('accounts.password_reset', token=token, _external=True)}

TBCOMP@DEV_GiorginoSerbuciano
	"""
	mail.send(msg)


@accounts.route('/passwordReset', methods=['GET', 'POST'])
def password_reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = ForgotPassword()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_password_reset_email(user)
		flash(
			'If this email corresponds to a registered account, you will shortly receive an email with a link to reset your password.',
			'info')
		print('Reset email sent to', user.email)
		return redirect(url_for('users.login'))
	return render_template('password_reset_request.html',
						   title='Reset Password',
						   form=form)


# PASSWORD IS RESET HERE
@accounts.route('/passwordReset/<token>', methods=['POST'])
def password_reset(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.validate_reset_token(token)
	if not user:
		flash('Invalid token!', 'warning')
		return redirect(url_for('accounts.password_reset_request'))
	form = PasswordReset()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pass
		flash('You\'ve set a new password!', 'success')
		return redirect(url_for('users.login'))
	return render_template('password_reset.html',
						   title='Set a new password',
						   form=form)

# END PASSWORD RESET
