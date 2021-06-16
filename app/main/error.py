from flask import render_template
from . import main

@main.app_errorhandler(404)
def error_handler(error):
    '''
    Function to render the 404 error page
    '''
    title = 'Not Found | Newsrun'
    return render_template('error.html', error_msg = error, title=title),404