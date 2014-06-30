from util.plugin import command
from util.pastes import post_gist


@command(name="analyze", help="Analyze and get statistics about a chat.", permission="command.analyze")
def inactive_search(chat, message, args, sender):
    if len(args) > 0:
        chat.SendMessage("No arguments required.")
        return
    messages = chat.Messages
    chat_length = len(messages)
    senders = {}
    for message in messages:
        handle = message.Sender.Handle
        if handle in senders:
            senders[handle] += 1
        else:
            senders[handle] = 1
    data = ''
    for user, amount in senders.items():
        data += u'%s:%s:%s\n' % (user, amount, percentage(amount, chat_length))
    url = post_gist(data)
    chat.SendMessage("Analysis output: %s" % url)


def percentage(part, whole):
    return 100 * float(part) / float(whole)



