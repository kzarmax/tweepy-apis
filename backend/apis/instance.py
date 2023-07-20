import configparser
import tweepy as tweepy
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

import backend.jsondb
import urllib.parse as urlparse


# Get tweepy instance with auth
class CustomTweepyClient(tweepy.Client):

    def c_get_bookmarks(self, **params):
        """c_get_bookmarks( \
            *, expansions=None, max_results=None, media_fields=None, \
            pagination_token=None, place_fields=None, poll_fields=None, \
            tweet_fields=None, user_fields=None \
        )

        customize get_books function of tweepy.Client
        """

        me = self.get_me()
        route = f"/2/users/{me.data.id}/bookmarks"

        return self._make_request(
            "GET", route, params=params,
            endpoint_parameters=(
                "expansions", "max_results", "media.fields",
                "pagination_token", "place.fields", "poll.fields", "bookmark.read", "bookmark.write",
                "tweet.fields", "user.fields"
            ), data_type=tweepy.Tweet
        )


class CustomOAuth2UserHandler(OAuth2Session):
    """OAuth 2.0 Authorization Code Flow with PKCE (User Context)
    authentication handler

    .. versionadded:: 4.5
    """

    def __init__(self, *, client_id, redirect_uri, scope, client_secret=None):
        super().__init__(client_id, redirect_uri=redirect_uri, scope=scope)
        if client_secret is not None:
            self.auth = HTTPBasicAuth(client_id, client_secret)
        else:
            self.auth = None

    def get_authorization_url(self):
        """Get the authorization URL to redirect the user to"""
        authorization_url, state = self.authorization_url(
            "https://twitter.com/i/oauth2/authorize",
            code_challenge=self._client.create_code_challenge(
                self._client.create_code_verifier(128), "S256"
            ), code_challenge_method="S256"
        )
        return authorization_url

    def get_code_verifier(self):
        return self._client.code_verifier

    def set_authorization_url(self, state, code_verifier):
        self._client.code_verifier = code_verifier
        self.authorization_url(
            "https://twitter.com/i/oauth2/authorize",
            state=state,
            code_challenge=self._client.create_code_challenge(
                code_verifier, "S256"
            ), code_challenge_method="S256"
        )

    def fetch_token(self, authorization_response):
        """After user has authorized the app, fetch access token with
        authorization response URL
        """
        return super().fetch_token(
            "https://api.twitter.com/2/oauth2/token",
            authorization_response=authorization_response,
            auth=self.auth,
            include_client_id=True,
            code_verifier=self._client.code_verifier
        )


def getinstance():
    config = configparser.ConfigParser()
    config.read('config.ini')

    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']
    bearer_token = config['twitter']['bearer_token']
    consumer_key = config['twitter']['consumer_key']
    consumer_secret = config['twitter']['consumer_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    client = CustomTweepyClient(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)
    return client


def fetch_auth_url_with_oauth2(username):
    config = configparser.ConfigParser()
    config.read('config.ini')
    client_id = config['twitter']['client_id']
    client_secret = config['twitter']['client_secret']

    # prepare OAuth2Handler
    oauth2_user_handler = CustomOAuth2UserHandler(
        client_id=client_id,
        redirect_uri="http://127.0.0.1:3000/callback",
        # minimal scope to work with bookmarks
        scope=["bookmark.read", "bookmark.write",
               "tweet.read", "users.read"],
        client_secret=client_secret
    )

    user = backend.jsondb.read_data()
    user["name"] = username
    user["authorization_url"] = oauth2_user_handler.get_authorization_url()

    query = urlparse.urlparse(user["authorization_url"]).query
    params = dict(urlparse.parse_qsl(query))
    user['state'] = params.get('state')
    user['code_verifier'] = oauth2_user_handler.get_code_verifier()

    oauth2_user_handler.state()
    backend.jsondb.write_data(user)

    print(user)
    return user["authorization_url"]


def set_pkce_of_user(verifier):
    config = configparser.ConfigParser()
    config.read('config.ini')
    client_id = config['twitter']['client_id']
    client_secret = config['twitter']['client_secret']

    # prepare OAuth2Handler
    oauth2_user_handler = CustomOAuth2UserHandler(
        client_id=client_id,
        redirect_uri="http://127.0.0.1:3000/callback",
        # minimal scope to work with bookmarks
        scope=["bookmark.read", "bookmark.write",
               "tweet.read", "users.read"],
        client_secret=client_secret,
    )

    user = backend.jsondb.read_data()
    oauth2_user_handler.set_authorization_url(user['state'], user['code_verifier'])

    access_token = oauth2_user_handler.fetch_token(verifier)

    user['access_token'] = access_token['access_token']
    backend.jsondb.write_data(user)

    # store these tokens in .env file:
    print(f"\naccess-token-pkce={user['access_token']}")
    return user['access_token']
