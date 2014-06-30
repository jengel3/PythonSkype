import random

from util.plugin import command


@command(name="choose", help="Choose a random item out of the provided choices.")
def choose(chat, message, args, sender):
    if len(args) == 0:
        chat.SendMessage("Specify at least one option.")
        return
    rand = random.randint(0, len(args) - 1)
    choice = args[rand]
    chat.SendMessage("I choose...%s" % choice)
