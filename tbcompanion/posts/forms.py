from flask_wtf.form import FlaskForm
from flask_login import current_user
from flask_pagedown.fields import PageDownField
from wtforms.fields.core import IntegerField, StringField
from wtforms.fields.simple import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from tbcompanion.models import Project, User


class PostForm(FlaskForm):
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
		project = Project.query.filter_by(id=project_id.data).first()
		if project and project.contributor != current_user:	# TODO Fix AttributeError: 'Project' object has no attribute 'contributor'
				raise ValidationError('You are not contributing to this project. Please leave a comment on the project\'s page instead.')
		elif not project:
			raise ValidationError('This project does not exist.')
