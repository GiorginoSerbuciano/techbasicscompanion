from flask_wtf.form import FlaskForm
from wtforms.fields.core import SelectField, StringField
from wtforms.fields.simple import SubmitField, TextAreaField
from wtforms.validators import URL, DataRequired, Length


class ProjectForm(FlaskForm):
	title = StringField('Title', validators=[
		DataRequired(),
		Length(min=2, max=80)
	])
	content = TextAreaField('Describe your project', validators=[
		DataRequired()
	])
	github_repo = StringField('URL to GitHub Repository', validators=[
		Length(max=120),
		URL('https://github.com/')
	])
	drop_tag = ['None', 'Art', 'Social', 'Data', 'Library', 'Meta', 'Other']
	tag = SelectField('Tag', choices=drop_tag, default=1)
	submit = SubmitField('Release project')
