import tweepy

from util.plugin import command
from util.plugin import event
from util.twitter_api import get_api
from util.twitter_api import get_auth
import config
import Skype4Py
import re

streams = {}


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

    chat.SendMessage(format_status(user_timeline[num]))


def format_status(status):
    return '@{}: {}'.format(status.user.screen_name, status.text)


@command(name="listen", help="Twitter live data stream")
def twitter_listen(chat, message, args, sender):
    if len(args) == 0:
        chat.SendMessage("Provide a user to listen to.")
        return
    api = get_api()
    if api is None:
        return
    user = api.get_user(args[0])
    if not user:
        chat.SendMessage("User not found")
        return
    conf = config.config()
    listens = conf.get('twitter_listens', None)
    if listens is None:
        conf['listens'] = {}
    if args[0] in listens:
        user_json = listens[args[0]]
        chats = user_json['chats']
        if chat.Name in chats:
            chat.SendMessage("This chat is already listening to that user's tweets!")
            return

    username_list = [args[0]]
    userids = []

    for username in username_list:
        user = api.get_user(screen_name=username)
        userids.append(str(user.id))
    streams.update({chat: args[0]})
    chat.SendMessage("Updated with new stream for {}".format(args[0]))
    args[0] = args[0].lower()
    if args[0] in listens:
        chats = listens[args[0]]['chats']
        chats.append(chat.Name)
        conf['listens'][args[0]]['chats'] = chats
    else:
        chats = [chat.Name]
        listens.update({args[0]: {}})
        conf['listens'][args[0]]['chats'] = chats
        conf['listens'][args[0]]['id'] = userids[0]

    config.save(conf)
    load_streams()


def get_chat_by_name(name):
    skype = Skype4Py.Skype()
    if not skype.Client.IsRunning:
        skype.Client.Start()
    skype.Attach()
    for chat_id in skype.Chats:
        if chat_id.Name == name:
            return chat_id


def load_streams():
    streams.clear()
    conf = config.config()
    users = conf.get("twitter_listens", {})
    userids = []
    for user in users:
        user_json = users[user]
        name = user_json['id']
        chats = user_json['chats']
        userids.append(name)
        for chat_id in chats:
            chat = get_chat_by_name(chat_id)
            streams.update({chat: user})
    if len(userids) == 0:
        return

    auth = get_auth()
    s = StreamWatcherListener()
    stream = tweepy.Stream(auth, s, timeout=None)
    stream.filter(follow=userids, async=True)


class StreamWatcherListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            chats_to_send = []
            for chat, user in streams.items():
                if user.lower() == status.author.screen_name.lower():
                    chats_to_send.append(chat)
            for chat in chats_to_send:
                chat.SendMessage(u'#TWEET UPDATE FOR @{}#\n{}'.format(status.author.screen_name, status.text))
        except:
            pass

    def on_error(self, status_code):
        from time import sleep
        print 'An error has occurred! Status code = %s' % status_code
        if str(status_code) == "420":
            print 'Waiting 3 seconds before restarting streams.'
            sleep(3000)
            load_streams()
            return False
        return True  # keep stream alive

    def on_timeout(self):
        print 'Streaming API timed out...'


@event(name='twitter_url', regex=r"(?:(?:www.twitter.com|twitter.com)/(?:[-_a-zA-Z0-9]+)/status/)([0-9]+)")
def twitter_url(chat, message, args, sender, found):
    match = re.search("(?:(?:www.twitter.com|twitter.com)/(?:[-_a-zA-Z0-9]+)/status/)([0-9]+)", message)
    tweet_id = match.group(1)
    api = get_api()
    try:
        tweet = api.get_status(tweet_id)
    except tweepy.error.TweepError:
        print("Failed to retrieve tweet data.")
        return

    chat.SendMessage(format_status(tweet))


confi = config.config()
env = confi.get("env", "production")
if env != "dev":
    load_streams()