from JakeBot import Command
import JakeBot


@Command(name="help", aliases="commands", help="Display a list of commands")
def choose(chat, message, args, sender):
    helps = {}
    for command, desc in JakeBot.command_helps.items():
        helps.update({command: desc})

    messages = ["Commands:"]
    for command, desc in helps.items():
        messages.append("* " + str(command) + " - " + str(desc))
    for message in messages:
        chat.SendMessage(message)