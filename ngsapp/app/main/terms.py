from flask import render_template

from ngsapp.app.main import main


@main.route('/terms-conditions')
def terms():
    return render_template('app/pages/main/terms-condition.html', title='Terms and condition')