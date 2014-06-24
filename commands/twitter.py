import tweepy

from util.plugin import command
from util.twitter import get_api
from util.twitter import get_auth

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

    chat.SendMessage('@{}: {}'.format(user.screen_name, user_timeline[num].text))


@command(name="listen", help="Twitter live data stream")
def twitter_listen(chat, message, args, sender):
    if len(args) == 0:
        chat.SendMessage("Provide a user to listen to.")
        return
    api = get_api()
    user = api.get_user(args[0])
    if not user:
        chat.SendMessage("User not found")
        return

    auth = get_auth()
    s = StreamWatcherListener()
    stream = tweepy.Stream(auth, s, timeout=None)
    username_list = [args[0]]
    userids = []

    for username in username_list:
        user = tweepy.API(auth).get_user(screen_name=username)
        userids.append(str(user.id))

    streams.update({chat: args[0]})
    stream.filter(follow=userids, async=True)
    print "Updated with new stream for " + args[0]


class StreamWatcherListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            chats_to_send = []
            for chat, user in streams.items():
                if user.lower() == status.author.screen_name.lower():
                    chats_to_send.append(chat)
            for chat in chats_to_send:
                chat.SendMessage('#TWEET UPDATE FOR @{}#\n{}'.format(status.author.screen_name, status.text))
        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'An error has occurred! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Streaming API timed out...'


