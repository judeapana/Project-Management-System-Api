from flask import render_template

from ngsapp.app.auth import auth


@auth.route('/reset-pwd/<token>')
def reset_pwd(token):
    return render_template('app/pages/auth/reset-pwd.html', title='Reset Password', token=token)
