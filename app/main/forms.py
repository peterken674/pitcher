from operator import imod
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required
from wtforms_sqlalchemy.fields import QuerySelectField
from ..models import Category
from flask_wtf.file import FileField, FileAllowed, FileRequired


class PitchForm(FlaskForm):
    pitch = TextAreaField('Tell us about you.', validators=[Required()], render_kw={"placeholder": "Type a pitch..."})
    category = QuerySelectField('Select category.', validators=[Required()], allow_blank=True, get_label='name')
    submit = SubmitField('Pitch')

class CommentForm(FlaskForm):
    comment = TextAreaField('',validators=[Required()], render_kw={"placeholder": "Type a comment..."})
    submit = SubmitField('Comment')

class UpdateProfilePic(FlaskForm):
    profile = FileField('Change Profile Picture', validators=[FileRequired(), FileAllowed(['jpg','png'], 'Images only allowed.')])
    submit = SubmitField('Change')

