from util.plugin import command


@command(name="marco", help='Polo!')
def marco(chat, message, args, sender):
    chat.SendMessage("Polo!")