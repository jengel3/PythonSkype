import glob
import os
import traceback
import sys
from util.permissions import load_permissions
import Skype4Py

from util import plugin

sys.path += ['commands']
version = 1.0  # Version number
chats = []


def reload_plugins(sky):
    fileset = set(glob.glob(os.path.join('commands', '*.py')))
    for filename in fileset:
        try:
            code = compile(open(filename, 'U').read(), filename, 'exec')
            namespace = {'skype': sky}
            eval(code, namespace)
        except Exception:
            traceback.print_exc()
            continue


def add_contact(user):
    user.IsAuthorized = True


if __name__ == "__main__":
    print("Starting SkypeBot %s" % version)
    load_permissions()
    skype = Skype4Py.Skype()

    if not skype.Client.IsRunning:
        skype.Client.Start()
    skype.Attach()
    print "Attached to Skype"

    skype.OnMessageStatus = plugin.dispatch
    skype.OnUserAuthorizationRequestReceived = add_contact
    print "Loaded API links."

    print "Loading chats..."
    for chat in skype.Chats:
        if chat.ActivityTimestamp > 3600 * 24 * 180:
            continue
        chats.append(chat)
    print "Chats loaded."

    reload_plugins(skype)
    print "Loaded plugins."

    print("Bot is loaded, and ready to go!")
