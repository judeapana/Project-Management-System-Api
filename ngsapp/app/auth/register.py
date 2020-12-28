from flask import render_template

from ngsapp.app.auth import auth


@auth.route('/register')
def register():
    return render_template('app/pages/auth/register.html', title='Register')
