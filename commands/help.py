from util import plugin
from util.plugin import command


@command(name="help", aliases="commands", help="Display a list of commands")
def choose(chat, message, args, sender):
    helps = {}
    for cmd, desc in plugin.command_helps.items():
        helps.update({cmd: desc})

    message = "Commands:\n"
    for cmd, desc in helps.items():
        message += "* " + str(cmd) + " - " + str(desc) + "\n"
    chat.SendMessage(message)