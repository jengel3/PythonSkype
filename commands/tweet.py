from JakeBot import Command
import tweepy
import JakeBot


def get_api():
    consumer_key = JakeBot.conf.get_value("twitter_api-key")
    consumer_secret = JakeBot.conf.get_value("twitter_api-key-secret")
    access_token_key = JakeBot.conf.get_value("twitter_access")
    access_token_secret = JakeBot.conf.get_value("twitter_access-secret")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    return tweepy.API(auth)


@Command(name="tweet", help="Twitter command")
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

    print "heree!!!!!!!!!"
    api = get_api()
    user = api.get_user(args[0])
    if not user:
        chat.SendMessage("User not found")
        return

    user_timeline = api.user_timeline(id=user.id, count=num + 1)

    if not user_timeline:
        chat.SendMessage("Timeline not found")
        return

    chat.SendMessage(user_timeline[num].text)



