from flask import render_template

from ngsapp.app.auth import auth


@auth.route('/login')
def login():
    return render_template('app/pages/auth/login.html', title='Login')
