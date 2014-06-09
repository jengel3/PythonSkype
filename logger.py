import datetime

FILE_NAME = 'log.txt'
MESSAGES_NAME = "messages.txt"


def log(message):
    print('[' + str(datetime.datetime.now())[:19] + '] ' + message)
    logfile = open(FILE_NAME, 'a')
    logfile.write('[' + str(datetime.datetime.now())[:19] + '] ' + message + '\n')
    logfile.close()


def log_message(skype_message):
    """

    :type skype_message: ChatMessage
    """
    print('[' + str(datetime.datetime.now())[:19] + '] {' + str(skype_message.Chat.Topic) + '} <' \
          + skype_message.Sender.FullName + '> ' + skype_message.Body)
    logfile = open(MESSAGES_NAME, 'a')
    logfile.write('[' + str(datetime.datetime.now())[:19] + '] {' + str(skype_message.Chat.Topic) + '} <'
                  + skype_message.Sender.FullName + '> ' + skype_message.Body + '\n')
    logfile.close()