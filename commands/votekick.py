from time import sleep
import thread

from util.plugin import command


vote_kicks = {}  # Chat to Kick


@command(name="votekick", help="Vote to kick a player")
def hi(chat, message, args, sender):
    """

    :type chat: Chat
    """
    if chat in vote_kicks:
        if len(args) != 1 and parse_choice(args[0]) is not None:
            chat.SendMessage("Use True/Yes or False/No to cast your vote!")
            return
        choice = parse_choice(args[0])
        vote_kicks[chat].vote(sender.Handle, choice)
        return
    if len(args) != 1:
        chat.SendMessage("Provide a user to votekick.")
        return
    username = args[0]
    found = False
    for user in chat.Members:
        if user.Handle.lower() == username.lower():
            found = True
    if not found:
        chat.SendMessage("Invalid user!")
        return
    new_kick = Kick(username, chat)

    vote_kicks.update({chat: new_kick})


class Kick:
    def __init__(self, user, chat):
        """

        :type chat: Chat
        """
        self.user = user
        self.chat = chat
        self.votes = {}
        thread.start_new_thread(self.start, ())

    def start(self):
        self.chat.SendMessage("Voting to kick {}. 20 Seconds remain.".format(self.user))
        sleep(10)
        self.chat.SendMessage("10 seconds remain.")
        sleep(5)
        self.chat.SendMessage("5 Seconds remain.")
        sleep(5)
        self.chat.SendMessage("Vote ending...")
        self.decide()

    def vote(self, user, choice):
        if user in self.votes:
            self.chat.SendMessage(user + ": You have already voted.")
            return
        self.votes.update({user: choice})
        self.chat.SendMessage(user + " voted " + str(choice))

    def decide(self):
        yesses = 0
        for vote, choice in self.votes.items():
            if choice:
                yesses += 1
        if yesses > 4:
            self.chat.SendMessage("The chat has voted to kick " + self.user)
            self.chat.Kick(self.user)
        else:
            self.chat.SendMessage("Not enough votes were received to kick " + self.user + ". Only " + str(yesses) +
                                  " yesses were received.")
        vote_kicks.pop(self.chat)


def parse_choice(choice):
    if choice.lower() == 'true' or choice.lower() == 'yes':
        return True
    elif choice.lower() == 'false' or choice.lower() == 'no':
        return False
    else:
        return None
