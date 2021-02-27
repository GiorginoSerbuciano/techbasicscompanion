from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.fields.core import BooleanField, SelectField, StringField
from wtforms.fields.simple import SubmitField, PasswordField, TextAreaField, TextField
from wtforms.validators import DataRequired, EqualTo, Length, Email, URL, ValidationError
from wtforms.widgets.core import CheckboxInput
from tbcompanion.models import User
from tbcompanion import bcrypt













