from util import plugin
from util.plugin import command
from util.pastes import post_gist


@command(name="help", aliases="commands", help="Display a list of commands")
def choose(chat, message, args, sender):
    helps = {}
    for cmd, desc in plugin.command_helps.items():
        helps.update({cmd: desc})

    message = "Commands:\n"
    for cmd, desc in helps.items():
        message += "* " + str(cmd) + " - " + str(desc) + "\n"
    url = post_gist(message)
    chat.SendMessage("Output: {}".format(url))