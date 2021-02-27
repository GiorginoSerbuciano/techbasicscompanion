from flask_wtf.form import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
	title = StringField('Title', validators=[
		DataRequired(),
		Length(max=120)
	])
	content = TextAreaField('Insert Text Here', validators=[
		DataRequired()
	])
	submit = SubmitField('Publish post')
