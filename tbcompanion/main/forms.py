from flask_wtf.form import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired


class SearchBox(FlaskForm):
	"""Placeholder for a future implementation"""

	string = StringField('Search for a post, user or project', validators=[
		DataRequired()])
	submit = SubmitField('Search')

