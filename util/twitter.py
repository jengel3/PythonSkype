import config
import tweepy


def get_api():
    return tweepy.API(get_auth())


def get_auth():
    consumer_key = config.get("twitter_api_key")
    consumer_secret = config.get("twitter_api_secret")
    access_token_key = config.get("twitter_access_key")
    access_token_secret = config.get("twitter_access_secret")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    return auth