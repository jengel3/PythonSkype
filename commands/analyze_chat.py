from plugin import command


@command(name="analyze", help="Find inactive users", permission="command.analyze")
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
    print "Completed analysis of chat."
    print "Writing statistics to file."
    text_file = open('chat-analysis.txt', 'a')
    for user, amount in senders.items():
        text_file.write(u'{}:{}:{}\n'.format(user, amount, percentage(amount, chat_length)))
    text_file.close()


def percentage(part, whole):
    return 100 * float(part) / float(whole)



