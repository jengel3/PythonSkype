# coding=utf-8
from util.plugin import command
import util.mcping as mcping
import re


@command(name='mcping', help='Ping a Minecraft server and get the response')
def mcping_command(chat, message, args, sender):
    port = 25565
    if len(args) == 0:
        chat.SendMessage("Provide an ip:port to ping.")
        return
    ip = args[0]
    split = ip.split(":")
    if len(split) == 2:
        try:
            port = int(split[1])
        except ValueError:
            chat.SendMessage("Invalid port number.")
            return
        ip = split[0]
    try:
        info = mcping.get_info(ip, port)
    except:
        chat.SendMessage("Unable to ping %s:%s" % (ip, port))
        return
    players_max = info['players']['max']
    players_online = info['players']['max']
    version_name = info['version']['name']
    motd = info['description'].encode('utf-8')
    motd_new = re.sub(re.compile(r"(?i)§[0-9A-FK-OR]"), '', motd)
    msg = u'Online Players: %s/%s | Version: %s | MOTD: %s' % (players_online, players_max, version_name, motd_new)
    chat.SendMessage(msg)