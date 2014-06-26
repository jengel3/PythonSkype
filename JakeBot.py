import glob
import os
import traceback
import sys
from util.permissions import load_permissions
import Skype4Py

from util import plugin

sys.path += ['commands']
version = 1.0  # Version number


def reload_plugins():
    fileset = set(glob.glob(os.path.join('commands', '*.py')))
    for filename in fileset:
        try:
            code = compile(open(filename, 'U').read(), filename, 'exec')
            namespace = {}
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
    reload_plugins()
    skype.OnMessageStatus = plugin.dispatch
    skype.OnUserAuthorizationRequestReceived = add_contact
    print("Commands have been loaded and the bot is running.")


