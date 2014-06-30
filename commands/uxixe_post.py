from util.plugin import command
from util.pastes import post_uxixe


@command(name='uxixe', help='Make a uxixe gist.')
def post_text(chat, message, args, sender):
    link = post_uxixe(' '.join(args))
    chat.SendMessage('%s: http://uxixe.com%s' % (sender.Handle, link))