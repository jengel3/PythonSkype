import Skype4Py
import glob
import os
import traceback
import logger
import config
import threading
import Queue
import sys
import inspect

sys.path += ['commands']


func_handlers = {}

commands = {}  # Name to function
command_permissions = {}  # Command to permission
command_helps = {}

events = {}  # Regex to function

user_permissions = {}  # Skype instance
version = 1.0  # Version number
source = ''  # Source link

conf = config.Config()  # Config instance

#
# Get argument data
#


def get_args_string(args):
    argstring = ""
    argiterator = iter(args)
    next(argiterator)
    for arg in argiterator:
        argstring += "{0} ".format(arg)
    return argstring


def get_args(args):
    argiterator = iter(args)
    next(argiterator)
    return list(argiterator)


def get_arg(num, args):
    argiterator = iter(get_args(args))
    while num > 0:
        next(argiterator)
        num -= 1
    return list(argiterator)


#
# Permissions Handling
#


def get_permissions(user):
    listed = []
    if not user in user_permissions:
        return listed
    perms = user_permissions[user]
    perm_string = perms.split(", ")
    for perm in perm_string:
        listed.append(perm)
    return listed


def has_permission(user, permission):
    perms = get_permissions(user)
    if permission in perms:
        return True
    else:
        return False


def add_permission(user, permission):
    perms = get_permissions(user)
    new_perms = []
    if len(perms) != 0:
        for perm in perms:
            new_perms.append(perm)
    new_perms.append(permission)
    perm_string = ''
    for perm in new_perms:
        perm_string += "%s, " % perm
    if len(perm_string) > 2:
        perm_string = perm_string[:-2]
    user_permissions.update({user: perm_string})


def remove_permission(user, permission):
    perms = get_permissions(user)
    new_perms = []
    if len(perms) != 0:
        for perm in perms:
            new_perms.append(perm)
    new_perms.remove(permission)
    perm_string = ''
    for perm in new_perms:
        perm_string += "%s, " % perm
    if len(perm_string) > 2:
        perm_string = perm_string[:-2]
    user_permissions.update({user: perm_string})


#
# Handles commands
#


def Command(arg=None, **kwargs):
    args = {}

    def wrapper(func):
        add_command(args, func)
        return func

    args.update({"name": kwargs.get('name', None)})
    args.update({"permission": kwargs.get('permission', None)})
    args.update({"aliases": kwargs.get('aliases', None)})
    args.update({"help": kwargs.get('help', None)})
    if kwargs or not inspect.isfunction(arg):
            if arg is not None:
                args['name'] = arg
            args.update(kwargs)
            return wrapper
    else:
        return wrapper(arg)


def load_plugins():
    fileset = set(glob.glob(os.path.join('commands', '*.py')))
    for filename in fileset:
        try:
            code = compile(open(filename, 'U').read(), filename, 'exec')
            namespace = {}
            eval(code, namespace)
        except Exception:
            traceback.print_exc()
            continue


def add_command(args, func):
    cmd = args['name']
    if cmd is None:
        print('No name found for a command..ignoring...')
        return
    registered_text = "Registered a command with the name '" + cmd + "'"
    new_command = {cmd: func}
    commands.update(new_command)
    if 'permission' in args and args['permission'] is not None:
        new_permission = {cmd: args['permission']}
        command_permissions.update(new_permission)
        registered_text += " with the permission " + str(new_permission.get(cmd))
    if 'help' in args and args['help'] is not None:
        new_help = {cmd: args['help']}
        command_helps.update(new_help)
        registered_text += " the help text of " + str(new_help.get(cmd))
    if 'aliases' in args and args['aliases'] is not None:
        aliases = args['aliases'].split(", ")
        for alias in aliases:
            commands.update({alias: func})
        registered_text += " and the aliases of " + str(list(aliases))
    logger.log(registered_text)
    handler = Handler(func)
    func_handlers.update({func: handler})


def dispatch(message, status):
    """

    :type message: ChatMessage
    """
    if (status == 'SENT' or status == 'RECEIVED') and message.Body.startswith('!'):
        # Get args and command from message
        args = message.Body.split()
        command = args[0].replace('!', "")
        # Check for valid command
        if not command in commands:
            message.Chat.SendMessage("Command not found!")
            return

        if command in command_permissions:
            permission = command_permissions[command]
            if not has_permission(message.Sender.Handle, permission):
                message.Chat.SendMessage("No permission to execute this command")
                return

        # Log command
        base = 'Received command \'{}\''.format(command)
        if len(get_args(args)) > 0:
            args = ' with arguments: {}'.format(get_args_string(args))
            base = base + args
        logger.log(base)
        # Execute command
        func = commands[command]
        handler = func_handlers[func]
        handler.add(message)


#
# Handles loading of config
#


def run(func, message):
    args = message.Body.split()
    func(message.Chat, message.Body, get_args(args), message.Sender)


class Handler(object):
    def __init__(self, func):
        self.func = func
        self.input_queue = Queue.Queue()
        self.thread = threading.Thread(name='handler-%s' % func.__name__, target=self.start)
        self.thread.start()

    def start(self):
        while True:
            message = self.input_queue.get()

            if message == StopIteration:
                break

            try:
                run(self.func, message)
            except:
                import traceback

                traceback.print_exc()

    def stop(self):
        self.input_queue.put(StopIteration)

    def add(self, message):
        self.input_queue.put(message)


print("Starting SkypeBot %s" % version)

skype = Skype4Py.Skype()
if not skype.Client.IsRunning:
    skype.Client.Start()
skype.Attach()
load_plugins()
skype.OnMessageStatus = dispatch


conf.load()
conf.set_default('twitter_api-key', '')
conf.set_default('twitter_api-secret', '')
conf.set_default('twitter_access', '')
conf.set_default('twitter_access-secret', '')
conf.save()

add_permission("jake0oo0", "command.hi")
add_permission("jake0oo0", "command.help")

print("Commands have been loaded and the bot is running.")

while True:
    raw_input('')