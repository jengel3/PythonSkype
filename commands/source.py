from util.plugin import command
import config

@command(name='source', help="Display a link to the bot's source.")
def source(chat, message, args, sender):
    conf = config.config()
    chat.SendMessage(conf.get('source'))