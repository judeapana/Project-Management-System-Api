from flask import render_template

from ngsapp.app.auth import auth


@auth.route('/forgot-pwd')
def forgot_pwd():
    return render_template('app/pages/auth/forgot-pwd.html', title='Forgot Password')
