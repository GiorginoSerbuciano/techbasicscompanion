from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.fields.core import BooleanField, StringField
from wtforms.fields.simple import SubmitField, PasswordField, TextAreaField, TextField
from wtforms.validators import DataRequired, EqualTo, Length, Email, URL, ValidationError
from tbcompanion.models import User
from tbcompanion import bcrypt


class RegistrationForm(FlaskForm):

	username = StringField('Username', validators = [
		DataRequired(),
		Length(min=5, max=20)		
	])
	email = StringField('Email', validators=[
		DataRequired(),
		Email()		
	])
	password = PasswordField('Password', validators=[
		DataRequired(),
		Length(min=8)	
	])
	confirm_password = PasswordField('Confirm Password', validators=[
		DataRequired(),
		EqualTo('password')
	])
	submit = SubmitField('Sign me up.')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exists.')
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is already in use.')	


class LoginForm(FlaskForm):
	
	#username not used for login
	email = StringField('Email', validators=[
		DataRequired(),
		Email()		
	])
	password = PasswordField('Password', validators=[
		DataRequired()	
	])
	submit = SubmitField('Log me in.')
	remember = BooleanField('Remember me.')


class ProjectForm(FlaskForm):

	title = StringField('Title', validators=[
		DataRequired(),
		Length(min=2, max=80)
	])
	content = TextAreaField('Insert Text Here', validators=[
		DataRequired()
	])
	github_repo = StringField('URL to GitHub Repository', validators=[
		Length(max=120),
		URL('https://github.com/')
	])
	submit = SubmitField('Release project')


class PostForm(FlaskForm):
	
	title = StringField('Title', validators=[
		DataRequired(),
	])
	content = TextAreaField('Insert Text Here', validators=[
		DataRequired()
	])
	submit = SubmitField('Publish post')



class UpdateAccount(FlaskForm):
	
	username = StringField('Username', validators = [
		DataRequired(),
		Length(min=5, max=20)		
	])
	email = StringField('Email', validators=[
		DataRequired(),
		Email()		
	])
	# password = PasswordField('Password', validators=[
	# 	DataRequired(),
	# 	Length(min=8)	
	# ])
	submit = SubmitField('Update my account.')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username already exists.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email is already in use.')	

	# def validate_password(self, password):
	# 	user = User.query.filter_by(email=password.data).first()
	# 	if not bcrypt.check_password_hash(user.password, password.data):
	# 		raise ValidationError('Wrong password.')	

