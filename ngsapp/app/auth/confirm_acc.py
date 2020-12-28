from flask import render_template

from ngsapp.app.auth import auth


@auth.route('/confirm-acc/<token>')
def confirm_acc(token):
    return render_template('app/pages/auth/confirm-acc.html', title='Confirm Account', token=token)
