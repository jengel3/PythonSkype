import urllib
import json

from plugin import command

check = u'\u2713'
nope = u'\u2717'


@command(name="mcstatus", help="Print Minecraft status")
def choose(chat, message, args, sender):
    chat.SendMessage(format_status())


def get_data():
    data = urllib.urlopen('http://status.mojang.com/check')
    return data.read()


def get_statuses():
    statuses = {}
    json_data = json.loads(get_data())
    for d in json_data:
        for key, value in d.iteritems():
            statuses.update({key: value})
    return statuses


def get_status(service):
    return get_statuses()['service']


def format_status():
    sb = ''
    for service, status in get_statuses().items():
        if status == 'green':
            sb += service + check + ' '
        else:
            sb += service + nope + ' '
    return sb