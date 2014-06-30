from util.plugin import command
import subprocess
import os


@command(name='ping', help='Ping an IP, with the output as you would see it in the command line.')
def ping_command(chat, message, args, sender):
    if len(args) != 1:
        chat.SendMessage("Provide an IP to ping.")
        return
    ip = args[0]
    if os.name == 'nt':
        process = subprocess.Popen('ping %s -n 3 -w 2000' % ip, stdout=subprocess.PIPE)
        out, err = process.communicate()
        chat.SendMessage(out)
    else:
        process = subprocess.Popen('ping %s -c 3 -w 2000' % ip, stdout=subprocess.PIPE)
        out, err = process.communicate()
        chat.SendMessage(out)