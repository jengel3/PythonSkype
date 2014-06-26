import urllib
import json
import config
import threading
import Skype4Py
from time import sleep

from util.plugin import command


check = u'\u2713'
nope = u'\u2717'

LISTEN_API = 'http://xpaw.ru/mcstatus/status.json'

listeners = []


@command(name="mcstatus", help="Print Minecraft status")
def choose(chat, message, args, sender):
    if len(args) == 1:
        if args[0].lower() == '--listen':
            listeners.append(chat.Name)
            conf = config.config()
            config_operators = conf.get('mc_listens', [])
            if chat.Name in config_operators:
                chat.SendMessage("This chat is already listening to Minecraft service statuses.")
                return
            config_operators.append(chat.Name)
            conf['mc_listens'] = config_operators
            config.save(conf)
        elif args[0].lower() == '--unlisten':
            conf = config.config()
            config_operators = conf.get('mc_listens', [])
            if chat.Name not in config_operators:
                chat.SendMessage("This chat is not currently listening to Minecraft service statuses.")
                return
            config_operators.remove(chat.Name)
            conf['mc_listens'] = config_operators
            config.save(conf)
        else:
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


def load_listeners():
    conf = config.config()
    chats = conf.get('mc_listens', [])
    for chat in chats:
        listeners.append(chat)


def start_listener():
    threading.Thread(target=listen)


def get_chat_by_name(name):
    skype = Skype4Py.Skype()
    if not skype.Client.IsRunning:
        skype.Client.Start()
    skype.Attach()
    for chat_id in skype.Chats:
        if chat_id.Name == name:
            return chat_id


previous_statuses = {}


def listen():
    while True:
        new_statuses = get_statuses()
        changed = []
        for service, status in new_statuses.items():
            old_status = previous_statuses[service]
            if status == old_status:
                continue
            else:
                changed.append(service)
        if len(changed) == 0:
            return
        else:
            sb = 'The following services have changed status: \n'
            for serv in changed:
                sb += '{} is now {}\n'.format(serv, new_statuses['serv'])
            for chat_id in listeners:
                chat = get_chat_by_name(chat_id)
                chat.SendMessage(sb)
        sleep(60)
