from JakeBot import Command
import JakeBot


@Command(name="help", aliases="commands", help="Display a list of commands")
def choose(chat, message, args, sender):
    helps = {}
    for command, desc in JakeBot.command_helps.items():
        helps.update({command: desc})

    message = "Commands:\n"
    for command, desc in helps.items():
        message += "* " + str(command) + " - " + str(desc) + "\n"
    chat.SendMessage(message)