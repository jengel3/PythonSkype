from util.plugin import command
from util.minecraft import verify
from util.minecraft import has_paid


@command(name='verify', help='Check if Minecraft credentials are valid.')
def verify_account(chat, message, args, sender):
    if len(args) != 2:
        chat.SendMessage("Specify a username and password.")
        return
    username = args[0]
    password = args[1]
    valid, migrated = verify(username, password)
    if valid:
        chat.SendMessage("Credentials are valid!")
    else:
        sb = 'Credentials are invalid!'
        if migrated is not None and migrated:
            sb += ' The account has been migrated.'
        chat.SendMessage(sb)


@command(name='haspaid', help='Check if a Minecraft user has paid.')
def haspaid(chat, message, args, sender):
    if len(args) != 1:
        chat.SendMessage("Specify a username.")
        return
    user = args[0]
    paid = has_paid(user)
    if paid:
        chat.SendMessage("{} is a premium username".format(user))
    else:
        chat.SendMessage("{} is not a premium username".format(user))