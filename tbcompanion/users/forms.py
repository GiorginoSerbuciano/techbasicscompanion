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