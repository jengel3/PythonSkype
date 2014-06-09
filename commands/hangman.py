from JakeBot import Command
import random
import re

full = "    0000000000000\n0           0\n0           1\n0          1 1\n0           1\n0          324\n0         " \
       "3 2 4\n0        3  2  4\n0          5 6\n0         5   6\n0        5     6\n0       5       6\n0\n0\n0"

guesses = 0
guessed = []
wrong = []
words = ('bukkit', 'mojang', 'notch', 'dinnerbone', 'mindcrack', 'hypixel', 'developer', 'java', 'programmer')
current_word = None
last_messages = []


@Command(name="hangman", aliases='hm', permission="command.hangman", help="Play Hangman in Skype!")
def hangman(chat, message, args, sender):
    if len(args) != 1 or len(args[0]) > 1 or not re.match("^[a-z]*$", args[0]):
        last_messages.append(chat.SendMessage('%s: You must provide a single letter as an argument.' % sender.Handle))
        return
    letter = args[0].lower()
    global current_word
    global guesses
    if current_word is None:
        current_word = words[random.randint(0, len(words) - 1)]
    for message in last_messages:
        if message is not None:
            message.Body = ''
            last_messages.remove(message)
    if letter in guessed:
        last_messages.append(chat.SendMessage('{}: The letter {} has already been guessed'.format(sender.Handle, letter)))
        return
    guessed.append(letter)
    if letter in current_word:
        last_messages.append(chat.SendMessage('{}: You have correctly guessed the letter: {}'.format(sender.Handle,
                                                                                                     letter)))
        last_messages.append(chat.SendMessage(get_message()))
        last_messages.append(chat.SendMessage("Guessed: {}".format(get_guessed())))
        last_messages.append(chat.SendMessage("Current Word: {}".format(get_needed())))
    else:
        wrong.append(letter)
        guesses += 1
        last_messages.append(chat.SendMessage('{}: You have incorrectly guessed the letter: {}'.format(sender.Handle,
                                                                                                       letter)))
        last_messages.append(chat.SendMessage(get_message()))
        last_messages.append(chat.SendMessage("Guessed: {}".format(get_guessed())))
        last_messages.append(chat.SendMessage("Current Word: {}".format(get_needed())))
    if guesses == 6:
        chat.SendMessage("The chat has lost Hangman! Use !hm <letter> to play again!")
        chat.SendMessage("The correct word was: " + current_word)
        guesses = 0
        current_word = words[random.randint(0, len(words) - 1)]
        del guessed[:]
    elif get_needed().replace(' ', '').lower() == current_word.lower():
        chat.SendMessage("The chat has won hangman! Use !hm <letter> to play again!")
        guesses = 0
        current_word = words[random.randint(0, len(words) - 1)]
        del guessed[:]
    else:
        return


def get_needed():
    will_return = ''
    for letter in current_word:
        temp_string = ' _ '
        if letter in guessed:
            temp_string = ' ' + letter + ' '
        will_return += temp_string
    return will_return


def get_guessed():
    to_send = ''
    for letter in guessed:
        to_send += letter + ", "
    return to_send


def get_message():
    if guesses == 0:
        return replace_all_except([0])
    temp_list = []
    temp_guess = 0
    while temp_guess <= guesses:
        temp_list.append(temp_guess)
        temp_guess += 1
    return replace_all_except(temp_list)


def replace_all_except(noreplace):
    temp = 0
    temp_message = full
    while temp <= 6:
        if temp in noreplace:
            temp += 1
            continue
        temp_message = temp_message.replace(str(temp), '')
        temp += 1
    return temp_message