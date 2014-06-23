import tweepy

from bot import config
from util.plugin import command


def get_api():
    consumer_key = config.get("twitter_api_key")
    consumer_secret = config.get("twitter_api_secret")
    access_token_key = config.get("twitter_access_key")
    access_token_secret = config.get("twitter_access_secret")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    return tweepy.API(auth)


@command(name="tweet", help="Twitter command")
def tweets(chat, message, args, sender):
    if len(args) == 0:
        chat.SendMessage("Provide a user")
        return

    num = 0
    if len(args) == 2:
        num = int(args[1])

    if num > 300:
        chat.SendMessage("Unable to process")
        return
    api = get_api()
    try:
        user = api.get_user(args[0])
        if not user:
            chat.SendMessage("User not found")
            return

        user_timeline = api.user_timeline(id=user.id, count=num + 1)
    except tweepy.error.TweepError:
        chat.SendMessage("Unable to find tweet.")
        return

    if not user_timeline:
        chat.SendMessage("Timeline not found")
        return

    chat.SendMessage('@{}: {}'.format(user.screen_name, user_timeline[num].text))



