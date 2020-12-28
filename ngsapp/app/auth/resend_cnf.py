from flask import render_template

from ngsapp.app.auth import auth


@auth.route('/resend-conf')
def resend_conf():
    return render_template('app/pages/auth/resend-conf.html', title='Resend Confirmation')
