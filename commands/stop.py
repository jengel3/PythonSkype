from util.plugin import command
import sys


@command(name='stop', help='Stop the bot.', aliases='end', permission='command.stop')
def stop(chat, message, args, sender):
    chat.SendMessage("Shutting down...")
    sys.exit(0)