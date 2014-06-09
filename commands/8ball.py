from JakeBot import Command
import random

responses = ("The answer is no.", "Uh, no.", "I Guess so.", "Yeah sure whatever.",
             "There comes a time when a man says no.", "Yeah, congratulations.",
             "Well, if I said yes, it would be a lie.", "Of Course.", "Yes.", "No.", "Without a doubt.",
             "My sources say no.", "As I see it, yes.", "You may rely on it.", "Not a chance.",
             "Outlook not so good.", "It is decidedly so.", "Was there ever any doubt?",
             "No, are you high?", "Very doubtful. ", "Yes - definitely.", "It is certain.",
             "Outlook good.", "Don't count on it.")


@Command(name="8ball", help="Ask the 8ball of its opinion!")
def eight_ball(chat, message, args, sender):
    if len(args) == 0:
        chat.SendMessage("Ask a question :(")
        return
    amount = len(responses)
    rand = random.randint(0, amount - 1)
    response = responses[rand]
    chat.SendMessage(sender.Handle + ": " + response)