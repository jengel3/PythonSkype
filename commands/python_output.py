from util.plugin import command

@command(name='python', permission='command.python')
def output(chat, message, args, sender):
    inp = ' '.join(args)
    try:
        chat.SendMessage(eval(inp))
    except:
        chat.SendMessage("Error executing code.")