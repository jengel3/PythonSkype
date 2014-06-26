from util.plugin import command
import os


@command(name='stop', help='Stop the bot.', aliases='end', permission='command.stop')
def stop(chat, message, args, sender):
    chat.SendMessage("Shutting down...")
    if os.name == 'nt':
        os.system('taskkill /F /IM python.exe /T')
        return
    os.system('killall python')