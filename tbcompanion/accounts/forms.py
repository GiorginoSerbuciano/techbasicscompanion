from flask_login import current_user
from flask_wtf.form import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
								ValidationError)

from tbcompanion.models import User


class RegistrationForm(FlaskForm):
	"""	This is the form used to register new users. See routes.register."""

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
		"""Check whether another user with the same USERNAME already exists in the database."""

		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exists.')

	def validate_email(self, email):
		"""Check whether another user with the same EMAIL ADDRESS already exists in the database."""

		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is already in use.')


class UpdateAccount(FlaskForm):
	"""This form allows users to update some account details. See routes.account_page."""

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
		"""Check whether another user with the same USERNAME already exists in the database."""

		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username already exists.')

	def validate_email(self, email):
		"""Check whether another user with the same USERNAME already exists in the database."""

		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email is already in use.')


class PasswordReset(FlaskForm):
	"""This form allows users to reset their password. See routes.password_reset."""

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
	"""This form is used in the password reset request process. See routes.password_reset_request"""

	email = StringField('Email', validators=[
		DataRequired(),
		Email()
	])
	submit = SubmitField('Reset my password.')
