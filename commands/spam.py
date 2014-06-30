from util.plugin import command
import Skype4Py


@command(name="spam", permission='command.spam')
def spam_command(chat, message, args, sender):
    if len(args) < 2:
        chat.SendMessage("Provide a user and message.")
        return
    user = args[0]
    msg = message.replace('!spam %s ' % user, '')
    spam(user, msg)


def spam(name, text, times=20):
    skype = Skype4Py.Skype()
    if not skype.Client.IsRunning:
        skype.Client.Start()
    skype.Attach()
    temp = 0
    while temp <= times:
        skype.SendMessage(name, text)
        temp += 1