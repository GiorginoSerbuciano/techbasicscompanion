from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
	# username not used for login
	email = StringField('Email', validators=[
		DataRequired(),
		Email()
	])
	password = PasswordField('Password', validators=[
		DataRequired()
	])
	submit = SubmitField('Log me in.')
	remember = BooleanField('Remember me.')
