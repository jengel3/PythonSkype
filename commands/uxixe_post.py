from util.plugin import command
from util.uxixe import post


@command(name='uxixe', help='Make a uxixe gist.')
def post_text(chat, message, args, sender):
    link = post(' '.join(args))
    chat.SendMessage('{}: http://uxixe.com{}'.format(sender.Handle, link))