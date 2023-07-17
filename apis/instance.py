import configparser
import tweepy as tweepy


# Get tweepy instance with auth
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

    api = tweepy.API(auth)
    client = tweepy.Client(bearer_token)
    return api, client

