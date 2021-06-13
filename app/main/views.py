from flask import render_template, redirect, url_for
from . import main

# Index page.
@main.route('/')
@main.route('/home')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home | Pitcher'

    return render_template('home.html', title = title)

@main.route('/comments')
def pitch():

    return render_template('comments.html')

@main.route('/profile')
def profile():

    return render_template('profile.html')