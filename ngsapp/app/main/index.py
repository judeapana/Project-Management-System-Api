from flask import render_template

from ngsapp.app.main import main


@main.route('/')
def index():
    return render_template('app/pages/main/index.html', title='App')
