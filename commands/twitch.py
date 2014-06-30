import util.http as http
from util.plugin import command
from util.plugin import event
import json
import re


CHANNEL_API = "https://api.twitch.tv/kraken/channels/%s"
STREAM_API = "https://api.twitch.tv/kraken/streams/%s"


@command(name='twitch', help="Retrieve info about a Twitch livestreamer.")
def twitch_command(chat, message, args, sender):
    if len(args) != 1:
        chat.SendMessage("Provide a streamer to search for.")
        return
    streamer = args[0]
    data = get_streamer_data(streamer)
    if data is None:
        chat.SendMessage("User not found.")
        return
    chat.SendMessage(data)


@event(name='twitch-regex', regex=r'(?:(?:www.twitch.tv|twitch.tv)\/)([-_a-zA-Z0-9]+)')
def twich_regex(chat, message, args, sender, found):
    match = re.search(r'(?:(?:www.twitch.tv|twitch.tv)/)([-_a-zA-Z0-9]+)', message)
    streamer = match.group(1)
    data = get_streamer_data(streamer)
    if data is None:
        return
    chat.SendMessage(data)


def get_streamer_data(streamer):
    stream = json.loads(http.get_url_data(STREAM_API % streamer))
    if 'error' in stream:
        return None
    online = stream.get('stream', None)
    if online is None:
        live = False
    else:
        live = True
    if live:
        data = stream['stream']
        viewers = data['viewers']
        game = data['game']
        chan = data['channel']
        status = chan['status']
        display = chan['display_name']
        followers = chan['followers']
        msg = '%s |LIVE|: %s - %s | Viewers: %s | Followers: %s' % (display, game, status, viewers, followers)
        return msg
    else:
        chan = json.loads(http.get_url_data(CHANNEL_API % streamer))
        game = chan['game']
        display = chan['display_name']
        views = chan['views']
        followers = chan['followers']
        msg = '%s |OFFLINE|: %s | Views: %s | Followers: %s' % (display, game, views, followers)
        return msg