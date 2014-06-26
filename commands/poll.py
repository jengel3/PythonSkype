from util.plugin import command
import collections

polls = {}  # Chat to poll


@command(name='poll', help='Start a poll.', permission='command.poll')
def poll_command(chat, message, args, sender):
    if len(args) == 0:
        chat.SendMessage("Provide a question and a list of possible responses.")
        return
    if args[0] == 'end':
        polls[chat].end_poll()
        return
    if chat in polls:
        chat.SendMessage("This chat already has an ongoing poll. Use '!poll end' to end it.")
        return
    split = message.split(' - ')
    if len(split) != 2:
        chat.SendMessage("Provide a message with the format '<question> - <choiceA>, <choiceB>, <etc>")
        return
    question = split[0].replace('!poll ', '')
    options = split[1]
    final_choices = []
    for option in options.split(', '):
        final_choices.append(option)
    if len(final_choices) == 0:
        chat.SendMessage("Provide options for the user to pick.")
        return
    poll = Poll(chat, final_choices, question, sender.Handle)
    polls.update({chat: poll})


@command(name='vote', help="Vote on the chat's current poll.")
def vote_command(chat, message, args, sender):
    if len(args) != 1:
        chat.SendMessage("Provide a choice to vote for")
        return
    if chat not in polls:
        chat.SendMessage("There is no ongoing poll in this chat.")
        return
    choice = args[0]
    poll = polls[chat]
    poll.vote(sender.Handle, choice)


class Poll:
    def __init__(self, chat, options, question, poller):
        self.chat = chat
        self.options = options
        self.question = question
        self.poller = poller
        self.votes = {}
        self.letter_choices = self.get_choice_list()
        self.start_poll()

    def start_poll(self):
        self.chat.SendMessage("{} has started a poll with the question '{}'. The choices are:\n {} "
                              "Use !vote <letter> to cast your vote.".format(self.poller, self.question,
                                                                             self.get_formatted_choices()))

    def end_poll(self, print_outcome=True):
        if not print_outcome:
            return
        polls.pop(self.chat)
        formatted_message = 'The results are in, and are as follows:\n'
        shown_choices = []
        for choice, count in self.count_votes().items():
            formatted_message += "{}: {} votes\n".format(self.letter_choices[choice], str(count))
            shown_choices.append(self.letter_choices[choice])
        for option in self.options:
            if option in shown_choices:
                continue
            shown_choices.append(option)
            formatted_message += "{}: {} votes\n".format(option, str(0))
        self.chat.SendMessage(formatted_message)

    def vote(self, voter, letter):
        if voter in self.votes:
            self.chat.SendMessage("{}: You have already voted".format(voter))
            return
        valid = self.is_valid_letter(letter)
        if not valid:
            self.chat.SendMessage("Invalid choice.")
            return
        self.votes.update({voter: letter})
        self.chat.SendMessage("{} has voted for letter {}".format(voter, letter))

    def is_valid_letter(self, letter):
        return letter in self.letter_choices

    def count_votes(self):
        counts = {}
        for choice in self.votes.values():
            if choice in counts:
                counts[choice] += 1
            else:
                counts[choice] = 1
        return counts

    def get_choice_list(self):
        choices = collections.OrderedDict()
        for choice in self.options:
            choice_letter = 'a'
            for letter in get_alphabet():
                if letter in choices:
                    continue
                else:
                    choice_letter = letter
                    break
            choices.update({choice_letter: choice})
        return choices

    def get_formatted_choices(self):
        choices = self.get_choice_list()
        choices_text = ''
        for letter, choice in choices.items():
            choices_text += "{}) {}\n".format(letter, choice)
        return choices_text


def get_alphabet(begin='a', end='z'):
    begin = ord(begin)
    end = ord(end)
    for number in xrange(begin, end+1):
        yield chr(number)