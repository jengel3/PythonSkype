from JakeBot import Command


@Command(name="hi", help="Say Hi!")
def hi(chat, message, args, sender):
    chat.SendMessage("Hi {}!".format(sender.FullName))
