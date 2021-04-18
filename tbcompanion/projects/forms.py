from urllib.parse import urlparse

from flask_login import current_user
from flask_pagedown.fields import PageDownField
from flask_wtf.form import FlaskForm
from wtforms.fields.core import SelectField, StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from tbcompanion.models import Project, User


class ProjectForm(FlaskForm):
	"""This is the form for creating a new project."""

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
		(None, 'None'),
		('art', 'Art'),
		('soc', 'Social'),
		('dat', 'Data'),
		('lib', 'Library'),
		('met', 'Meta'),
		('etc', 'Other')]
	tag = SelectField('Tag', choices=dropdown_tags)
	submit = SubmitField('Release project')

	def validate_github_repo(self, github_repo):
		"""Checks that the given URL is valid, i.e. links to a Github repository."""

		project = Project.query.filter_by(github_repo=github_repo.data).first()
		parse = urlparse(github_repo.data)

		"""Raise ValidationError if a different project has this repository assigned to it,
		   i.e. the user is attempting to create a duplicate project,
		   or if either the scheme or domain do not match to Github's"""
		if project:
			raise ValidationError('''This GitHub repository is linked to a different project.
								  Please update the already-existing project if you are a contributor.''')
		elif parse.scheme != 'https' or parse.netloc != 'github.com':
			raise ValidationError('Invalid URL.')

	def validate_contributors(self, contributors):
		"""Checks that the given contributors exist."""

		contributors_list = contributors.data.split(', ')

		if len(contributors_list) > 1:  # Only possible if the list is not empty.
			for c in contributors_list:
				user = User.query.filter_by(id=c).first()
				if not user:
					raise ValidationError(f'User ID "{c}" does not exist!')
				elif user == current_user:
					raise ValidationError(f'No need to pass yourself as a contributor ;).')


