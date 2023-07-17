import configparser
import tweepy as tweepy

bearer_token = "AAAAAAAAAAAAAAAAAAAAAKpdowEAAAAASKe45beYJj1twAo7uviBdRR902Q%3DoJFKGC7wvnlhYpbiyJnp7jEvq72Izejmi00j6wa9OGHooY2ccZ"
consumer_key = "dLQ22oUBY2XKvyxqKSkeeRb0V"
consumer_secret = "I1zw4guYRF7lj7P8sxQ6JXoCGYpKoLpx0QDwqkevJR05mzf9Rm"
access_token = "1509021912202055681-gsik1bUjl3Dq0HuhTeuo20Rg9SmALJ"
access_token_secret = "hrs2EtBYrNQldk7ItVKGVXivO0n6nGBcpzJQGFdwgLcQc"


# Get tweepy instance with auth
def getinstance():
    config = configparser.ConfigParser()
    config.read('config.ini')

    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']
    bearer_token = config['twitter']['bearer_token']
    client_id = config['twitter']['client_id']
    client_id_secret = config['twitter']['client_id_secret']

    client = tweepy.Client(
        bearer_token,
        consumer_key=client_id,
        consumer_secret=client_id_secret,
        access_token,
        access_token_secret,
    )

    return client
