from operator import imod
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required
from wtforms_sqlalchemy.fields import QuerySelectField
from ..models import Category


class PitchForm(FlaskForm):
    pitch = TextAreaField('New Pitch', validators=[Required()])
    category = QuerySelectField('Category', validators=[Required()], allow_blank=True, get_label='name')
    submit = SubmitField('Pitch')