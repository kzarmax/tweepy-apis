import os

from flask import Flask
from flask import request
import tweepy

from backend.apis.instance import set_pkce_of_user
from backend.index import fetch_pkce

# from backend.main import get_me

app = Flask(__name__, static_folder='./frontend/build', static_url_path='/')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.errorhandler(tweepy.errors.BadRequest)
def handle_bad_request(e):
    return 'Invalid Username! Refresh Page to try again'


@app.route('/api/<username>')
def serve(username):
    # Get the ID of the user
    print(username)
    return fetch_pkce(username)


@app.route('/callback')
def callback():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    print(request.url)
    set_pkce_of_user(request.url)
    return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 3000))
