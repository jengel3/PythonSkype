import datetime

FILE_NAME = 'log.txt'
MESSAGES_NAME = "messages.txt"


def log(message):
    """

    :type message: String
    """
    msg = u'[%s] %s' % (str(datetime.datetime.now())[:19], message)
    print(msg)
    logfile = open(FILE_NAME, 'a')
    logfile.write(msg.encode("UTF-8") + '\n')
    logfile.close()


def log_message(skype_message):
    """

    :type skype_message: ChatMessage
    """
    msg = u'[%s] %s <%s> %s' % (str(datetime.datetime.now())[:19], str(skype_message.Chat.Topic),
                                skype_message.Sender.Handle, skype_message.Body)
    print(msg)
    logfile = open(MESSAGES_NAME, 'a')
    logfile.write(msg.encode("UTF-8") + '\n')
    logfile.close()