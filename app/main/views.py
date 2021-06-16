from ..models import Category, Pitch, Comment, User
from flask import render_template, redirect, url_for, request
from . import main
from flask_login import login_required, current_user
from .forms import CommentForm, PitchForm, UpdateProfilePic
from sqlalchemy import desc
from .. import photos, db


# Index page.
@main.route('/', methods = ['GET', 'POST'])
def index():
    '''
    View root page function that returns the index page and its data
    '''
    pitches = Pitch.get_pitches()
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

    

    return render_template('home.html', title = title, form=form, pitches = pitches)

@main.route('/<int:id>', methods = ['GET', 'POST'])
def categories(id):
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

    pitches = Pitch.get_pitches_by_category(id)
    return render_template('home.html', title = title, form=form, pitches = pitches)

@main.route('/<pitch_id>/comments', methods = ['GET', 'POST'])
def comment(pitch_id):

    comment_form = CommentForm()
    title = 'Comments | Pitcher'
    pitch = Pitch.query.filter_by(id=pitch_id).first()
    # Get comments for pitch.
    comments = Comment.get_comments(pitch_id)
    if comment_form.validate_on_submit():
        comment = comment_form.comment.data

        new_comment = Comment(comment=comment, user=current_user, pitch=pitch)
        new_comment.save_comment()
        return redirect(request.referrer)

    return render_template('comments.html', pitch=pitch, form=comment_form, comments=comments, title=title)

@main.route('/user/profile/<int:id>', methods = ['GET', 'POST'])
@login_required
def profile(id):

    form = UpdateProfilePic()
    user = User.query.filter_by(id=id).first()
    pitches = Pitch.get_pitches_by_user(id)

    title = '{} {} | Profile'.format(user.fname, user.lname)

    if form.validate_on_submit():
        filename = photos.save(form.profile.data)
        profile_pic_path = f'img/{filename}'
        user.profile_pic_path = profile_pic_path
        db.session.commit()
        return redirect(url_for('main.profile', id=id))

    return render_template('profile.html', pitches=pitches, form=form, user=user, title=title)

@main.route('/like/<int:id>/<action>', methods = ['GET', 'POST'])
@login_required
def like_action(id, action):
    pitch = Pitch.query.filter_by(id=id).first_or_404()
    if action == 'like':
        current_user.like_pitch(pitch)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_pitch(pitch)
        db.session.commit()
    return redirect(request.referrer)

@main.route('/like/comment/<int:id>/<action>', methods = ['GET', 'POST'])
@login_required
def like_comment_action(id, action):
    comment = Comment.query.filter_by(id=id).first_or_404()
    if action == 'like':
        current_user.like_comment(comment)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_comment(comment)
        db.session.commit()
    return redirect(url_for('main.comment', pitch_id = comment.pitch.id))
