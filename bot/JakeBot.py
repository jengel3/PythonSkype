import glob
import os
import traceback
import sys

import Skype4Py

from util import plugin


sys.path += ['commands']


version = 1.0  # Version number
source = 'https://github.com/Jake0oo0/PythonSkype'  # Source link


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


def main():
    print("Starting SkypeBot %s" % version)

    skype = Skype4Py.Skype()
    if not skype.Client.IsRunning:
        skype.Client.Start()
    skype.Attach()
    reload_plugins()
    skype.OnMessageStatus = plugin.dispatch

    print("Commands have been loaded and the bot is running.")


if __name__ == "__main__":
    main()