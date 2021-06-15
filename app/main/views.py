from app.models import Category, Pitch, Comment
from flask import render_template, redirect, url_for
from . import main
from flask_login import login_required, current_user
from .forms import CommentForm, PitchForm
from sqlalchemy import desc

# Index page.
@main.route('/', methods = ['GET', 'POST'])
def index():
    '''
    View root page function that returns the index page and its data
    '''
    form = PitchForm()
    title = 'Home | Pitcher'
    form.category.query = Category.query
    if form.validate_on_submit():
        selected_category = form.category.data
        pitch = form.pitch.data

        new_pitch = Pitch(pitch=pitch, user=current_user, category=selected_category)

        # Save Pitch
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    pitches = Pitch.query.order_by(desc(Pitch.posted)).all()

    return render_template('home.html', title = title, form=form, pitches = pitches)

@main.route('/<int:id>', methods = ['GET', 'POST'])
def categories(id):
    '''
    View root page function that returns the index page and its data
    '''
    form = PitchForm()
    title = 'Home | Pitcher'
    form.category.query = Category.query
    pitches = []
    if form.validate_on_submit():
        selected_category = form.category.data
        pitch = form.pitch.data

        new_pitch = Pitch(pitch=pitch, user=current_user, category=selected_category)

        # Save Pitch
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    pitches = Pitch.get_pitches_by_category(id)

    return render_template('home.html', title = title, form=form, pitches = pitches)

@main.route('/<pitch_id>/comments', methods = ['GET', 'POST'])
def comment(pitch_id):

    comment_form = CommentForm()
    title = 'Comments | Pitcher'
    pitch = Pitch.query.filter_by(id=pitch_id).first()
    if comment_form.validate_on_submit():
        comment = comment_form.comment.data

        new_comment = Comment(comment=comment, user=current_user, pitch=pitch)
        new_comment.save_comment()
        return redirect(url_for('main.comment', pitch_id=pitch_id))

    # Get comments for pitch.
    comments = Comment.get_comments(pitch_id)
    return render_template('comments.html', pitch=pitch, form=comment_form, comments=comments, title=title)

@main.route('/profile')
@login_required
def profile():

    return render_template('profile.html')
