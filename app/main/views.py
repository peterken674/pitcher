from app.models import Category, Pitch
from flask import render_template, redirect, url_for
from . import main
from flask_login import login_required, current_user
from .forms import PitchForm
from sqlalchemy import desc

# Index page.
@main.route('/', methods = ['GET', 'POST'])
@main.route('/home', methods = ['GET', 'POST'])
def index():
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

    pitches = Pitch.query.order_by(desc(Pitch.posted)).all()
    return render_template('home.html', title = title, form=form, pitches = pitches)

@main.route('/comments')
def pitch():

    return render_template('comments.html')

@main.route('/profile')
def profile():

    return render_template('profile.html')
