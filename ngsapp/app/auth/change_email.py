from flask import render_template

from ngsapp.app.auth import auth


@auth.route('/change-email/<token>')
def change_email(token):
    return render_template('app/pages/auth/change-email.html', title='Change Email Address', token=token)
