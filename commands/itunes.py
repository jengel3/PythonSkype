from util.plugin import command
import urllib
from util.http import get_url_data
import json

api_url = "https://itunes.apple.com/search?term={}"


@command(name='itunes', help='Get info about a iTunes song.')
def itunes_command(chat, message, args, sender):
    if len(args) == 0:
        chat.SendMessage("Provide a query.")
        return
    query = ' '.join(args)
    query = urllib.quote(query)
    formatted_url = api_url.format(query)
    json_data = json.loads(get_url_data(formatted_url))
    if 'results' not in json_data:
        chat.SendMessage("Unable to find a match.")
        return
    results = json_data['results']
    result = results[0]
    if result is None:
        chat.SendMessage("Unable to find a match.")
        return
    track = result['trackName']
    artist = result['artistName']
    album = result['collectionName']
    link = result['trackViewUrl']
    msg = "Track: {} | Artist: {} | Album: {} | {}".format(track, artist, album, link)
    chat.SendMessage(msg)