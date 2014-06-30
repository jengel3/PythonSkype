import random

from util.plugin import command
from util.data_utils import get_lines

responses = get_lines('8ball.txt')


@command(name="8ball", help="Ask the 8ball of its opinion!")
def eight_ball(chat, message, args, sender):
    if len(args) == 0:
        chat.SendMessage("Ask a question :(")
        return
    amount = len(responses)
    rand = random.randint(0, amount - 1)
    response = responses[rand]
    chat.SendMessage("%s: %s" % (sender.Handle, response))