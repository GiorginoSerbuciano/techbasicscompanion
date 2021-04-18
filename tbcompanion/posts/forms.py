from flask_login import current_user
from flask_pagedown.fields import PageDownField
from flask_wtf.form import FlaskForm
from wtforms.fields.core import IntegerField, StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from tbcompanion.models import Project


class PostForm(FlaskForm):
	"""This is the form used to create new posts."""

	title = StringField('Title', validators=[
		DataRequired(),
		Length(max=120)
	])
	content = PageDownField('Insert Text Here', validators=[
		DataRequired()
	])
	project_id = IntegerField('This post is related to project-ID:', validators=[
		DataRequired(),
	])
	submit = SubmitField('Publish post')

	def validate_project_id(self, project_id):
		"""Check that 'project_id.data' corresponds to the ID of any existing project in the database."""

		project = Project.query.filter_by(id=project_id.data).first()

		"""Raise ValidationError if the project exists but the current user is not a contributor,
		   or if the project does not exist."""
		if project and project.contributor != current_user:
			raise ValidationError('You are not contributing to this project. '
								  'Please leave a comment on the project\'s page instead.')
		elif not project:
			raise ValidationError('This project does not exist.')
