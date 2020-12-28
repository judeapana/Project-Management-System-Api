from ngsapp.app.client import client


@client.route('/')
def dashboard():
    return 'Hello'
