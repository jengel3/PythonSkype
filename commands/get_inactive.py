import datetime
import calendar
from util.pastes import post_gist

from util.plugin import command


@command(name="inactive", help="Find inactive users", permission="command.inactive")
def inactive_search(chat, message, args, sender):
    if len(args) > 0:
        chat.SendMessage("No arguments required.")
        return
    messages = chat.Messages
    print len(messages)
    chat_members = []
    for member in chat.Members:
        chat_members.append(member.Handle)
    print chat_members
    active_members = []
    oldest = datetime.datetime.now()
    for message in messages:
        if message.Datetime < sub_months(datetime.datetime.now(), 2):
            oldest = message.Datetime
            continue
        handle = message.Sender.Handle
        if handle not in chat_members:
            continue
        if handle not in active_members:
            active_members.append(handle)
            print "Found active user {}".format(handle)
        if len(active_members) == len(chat_members):
            print "ALL users are active in the chat!"
            break
    print "Completed analysis of chat."
    print "Printing inactive members that have not posted in the last two months:"
    data = ''
    for user in chat_members:
        if user not in active_members:
            data += user + '\n'
    chat.SendMessage(post_gist(data))
    print "OLDEST: " + str(oldest)


def sub_months(sourcedate, months):
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(year, month, day)



