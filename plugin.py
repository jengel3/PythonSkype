import logger
import inspect
import utils
import traceback
import threading
import Queue
import permissions
import re

func_handlers = {}
commands = {}  # Name to function
command_permissions = {}  # Command to permission
command_helps = {}

events = {}  # Name to function
event_regex = {}  # Name to regex


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


def register_event(args, func):
    name = args['name']
    regex = args['regex']
    if name is None or regex is None:
        print "No {} found for an event...skipping...".format('regex' if regex is None else 'name')
        return
    registered_text = "Registered an event with the name '{}' and the regex: {}".format(name, regex)
    new_event = {name: func}
    events.update(new_event)
    new_regex = {name: re.compile(regex)}
    event_regex.update(new_regex)
    handler = Handler(func)
    func_handlers.update({func: handler})
    logger.log(registered_text)


def command(arg=None, **kwargs):
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


def event(arg=None, **kwargs):
    args = {}

    def wrapper(func):
        register_event(args, func)
        return func

    args.update({"name": kwargs.get('name', None)})
    args.update({"regex": kwargs.get('regex', None)})

    if kwargs or not inspect.isfunction(arg):
        if arg is not None:
            args['name'] = arg
        args.update(kwargs)
        return wrapper
    else:
        return wrapper(arg)


def dispatch(message, status):
    """

    :type message: ChatMessage
    """
    if status == 'SENT' or status == 'RECEIVED':
        for e in events:
            func = events[e]
            regex = event_regex[e]
            f = re.findall(regex, message.Body)
            if len(f) > 0:
                for found in f:
                    handler = func_handlers[func]
                    handler.add({'data': message, 'type': 'event', 'extra': {'found': found}})
                return
        if not message.Body.startswith('!'):
            return
        # Get args and command from message
        args = message.Body.split()
        cmd = args[0].replace('!', "")
        # Check for valid command
        if not cmd in commands:
            message.Chat.SendMessage("Command not found!")
            return

        if cmd in command_permissions:
            permission = command_permissions[cmd]
            if not permissions.has_permission(message.Sender.Handle, permission):
                message.Chat.SendMessage("No permission to execute this command")
                return

        # Log command
        base = 'Received command \'{}\''.format(cmd)
        if len(utils.get_args(args)) > 0:
            args = ' with arguments: {}'.format(utils.get_args_string(args))
            base = base + args
        logger.log(base)
        # Execute command
        func = commands[cmd]
        handler = func_handlers[func]
        handler.add({'data': message, 'type': 'command'})


def run(func, args):
    extra = args.get('extra', None)
    message = args['data']
    command_args = message.Body.split()
    t = args['type']
    if t == 'command':
        func(message.Chat, message.Body, utils.get_args(command_args), message.Sender)
    elif t == 'event':
        found = extra['found']
        func(message.Chat, message.Body, utils.get_args(command_args), message.Sender, found)


class Handler(object):
    def __init__(self, func):
        self.func = func
        self.input_queue = Queue.Queue()
        self.thread = threading.Thread(name='handler-%s' % func.__name__, target=self.start)
        self.thread.start()

    def start(self):
        while True:
            args = self.input_queue.get()

            if args == StopIteration:
                break

            try:
                run(self.func, args)
            except:
                import traceback

                traceback.print_exc()

    def stop(self):
        self.input_queue.put(StopIteration)

    def add(self, message):
        self.input_queue.put(message)
