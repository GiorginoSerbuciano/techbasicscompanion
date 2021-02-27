from flask_login import current_user
from flask_wtf.form import FlaskForm
from tbcompanion.models import User
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[
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


class UpdateAccount(FlaskForm):
	username = StringField('Username', validators=[
		DataRequired(),
		Length(min=5, max=20)
	])
	email = StringField('Email', validators=[
		DataRequired(),
		Email()
	])
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


class PasswordReset(FlaskForm):
	password = PasswordField('Password', validators=[
		DataRequired(),
		Length(min=8)
	])
	confirm_password = PasswordField('Confirm Password', validators=[
		DataRequired(),
		EqualTo('password')
	])
	submit = SubmitField('Change my password.')


class ForgotPassword(FlaskForm):
	email = StringField('Email', validators=[
		DataRequired(),
		Email()
	])
	submit = SubmitField('Reset my password.')
