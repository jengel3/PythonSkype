import config
import tweepy


def get_api():
    return tweepy.API(get_auth())


def get_auth():
    conf = config.config()
    consumer_key = conf.get("keys", {}).get("twitter_api_key", None)
    consumer_secret = conf.get("keys", {}).get("twitter_api_secret", None)
    access_token_key = conf.get("keys", {}).get("twitter_access_key", None)
    access_token_secret = conf.get("keys", {}).get("twitter_access_secret", None)
    if consumer_key is None or consumer_secret is None or access_token_key is None or access_token_secret is None:
        return None
    auth = tweepy.OAuthHandler(bytes(consumer_key), bytes(consumer_secret))
    auth.set_access_token(bytes(access_token_key), bytes(access_token_secret))
    return auth