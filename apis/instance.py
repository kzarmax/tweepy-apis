import configparser
import tweepy as tweepy


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


def fetch_pkce_with_oauth2():
    config = configparser.ConfigParser()
    config.read('config.ini')
    client_id = config['twitter']['client_id']
    client_secret = config['twitter']['client_secret']

    # prepare OAuth2Handler
    oauth2_user_handler = tweepy.OAuth2UserHandler(
        client_id=client_id,
        redirect_uri="https://127.0.0.1:6006/callback",
        # minimal scope to work with bookmarks
        scope=["bookmark.read", "bookmark.write",
               "tweet.read", "users.read"],
        client_secret=client_secret
    )

    print(oauth2_user_handler.get_authorization_url())

    verifier = input("Enter whole callback URL: ")

    access_token = oauth2_user_handler.fetch_token(
        verifier
    )

    # store these tokens in .env file:
    print(f"\naccess-token-pkce={access_token['access_token']}")
