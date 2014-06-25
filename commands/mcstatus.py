import urllib
import json

from util.plugin import command


check = u'\u2713'
nope = u'\u2717'


@command(name="mcstatus", help="Print Minecraft status")
def choose(chat, message, args, sender):
    if len(args) == 1:
        service = args[0]
        if service in get_statuses():
            chat.SendMessage(format_status(service))
            return
        else:
            chat.SendMessage("Service not found.")
            return
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


def format_status(check_service=None):
    sb = ''
    for service, status in get_statuses().items():
        if check_service is not None and service != check_service:
            continue
        if status == 'green':
            sb += service + check + ' '
        else:
            sb += service + nope + ' '
        if check_service is not None and service == check_service:
            return sb
    return sb