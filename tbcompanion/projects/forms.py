from flask_wtf.form import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms.fields.core import SelectField, StringField
from wtforms.fields.simple import SubmitField, TextAreaField
from wtforms.validators import URL, DataRequired, Length, ValidationError
from tbcompanion.models import Project, User
from urllib.parse import urlparse


class ProjectForm(FlaskForm):
	title = StringField('Title', validators=[
		DataRequired(),
		Length(min=2, max=80)
	])
	content = PageDownField('Describe your project', validators=[
		DataRequired()
	])
	github_repo = StringField('URL to GitHub Repository', validators=[
		Length(max=120),
	])
	contributors = StringField('List contributors in the format "User1, User2, User3"')
	dropdown_tags = [
		(None,'None'), 
		('art','Art'), 
		('soc','Social'), 
		('dat','Data'),
		('lib','Library'),
		('met','Meta'),
		('etc','Other')]
	tag = SelectField('Tag',choices=dropdown_tags)
	submit = SubmitField('Release project')
	
#TODO: #8 Add contributors

	def validate_github_repo(self, github_repo):
		project = Project.query.filter_by(github_repo=github_repo.data).first()
		parse = urlparse(github_repo.data)
		if project:
			raise ValidationError('This GitHub repository is linked to a different project. Please update the already-existing project if you are a contributor.')
		elif parse.scheme != 'https' or parse.netloc != 'github.com':
			raise ValidationError('Invalid URL.')

	def validate_contributors(self, contributors):
		contributors_list = contributors.data.split(', ')
		if len(contributors_list) > 1:
			for contributor in contributors_list:
				user = User.query.filter_by(username=contributor).first()
				if not user:
					raise ValidationError(f'The user "{contributor}" does not exist!')
				elif user == current_user:
					raise ValidationError(f'No need to pass yourself as a contributor ;).')