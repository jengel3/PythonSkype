from util.plugin import command


@command(name="hi", help="Say Hi!")
def hi(chat, message, args, sender):
    chat.SendMessage(u"Hi %s!" % sender.Handle)
