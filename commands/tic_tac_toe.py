from util.plugin import command
from util.string_utils import get_random_string

render = "A | {} | {} | {} |\n" \
         "   --------------\n" \
         "B | {} | {} | {} |\n" \
         "   --------------\n" \
         "C | {} | {} | {} |\n" \
         "     1    2    3 " \

# !ttt start josh0309
# !ttt move a3
# !ttt quit
games = {}


@command(name='ttt', help="Play Tic tac toe with a friend! Start a game with !ttt start <user>")
def tic_tac_toe(chat, message, args, sender):
    if len(args) == 0:
        chat.SendMessage("Provide an argument.")
        return
    if args[0] == "start":
        if len(args) != 2:
            chat.SendMessage("Provide a partner.")
            return
        game = TicTacToe(chat, sender.Handle, args[1])
        games.update({game.id: game})
        chat.SendMessage("Started game.\n{}, use !ttt move <column|row> to move. For example: !ttt move a3"
                         .format(game.move))
    elif args[0] == "end":
        game = get_game_by_sender(chat, sender.Handle)
        if game is None:
            chat.SendMessage("No game exists.")
            return
        games.pop(game.id)
    elif args[0] == "move":
        if len(args) != 2:
            chat.SendMessage("Provide a column and row.")
            return
        if len(args[1]) != 2:
            chat.SendMessage("Provide a row and column in a single argument. eg. e3")
            return
        move = args[1].lower()
        game = get_game_by_sender(chat, sender.Handle)
        if game is None:
            chat.SendMessage("You do not have a running game.")
            return
        remove = game.make_move(sender.Handle, move[1], move[0])
        if remove:
            games.pop(game.id)


def get_game_by_sender(chat, sender):
    for game in games.values():
        if (game.user == sender or game.partner == sender) and chat == game.chat:
            return game


class TicTacToe:
    def __init__(self, chat, user, partner):
        self.chat = chat
        self.user = user
        self.partner = partner
        self.move = partner
        self.id = get_random_string(6)
        self.rows = ['a', 'b', 'c']
        self.columns = ['1', '2', '3']
        self.current_tiles = [-1, -1, -1,  # -1 = Space
                              -1, -1, -1,  # 0 = O
                              -1, -1, -1]  # 1 = X

    def make_move(self, handle, column, row):
        if handle != self.user and handle != self.partner:
            return False
        if self.move != handle:
            self.chat.SendMessage("It is not your move!")
            return
        space = self.get_space(column, row)
        if space is None:
            self.chat.SendMessage("Invalid tile.")
            return
        if self.current_tiles[space] != -1:
            self.chat.SendMessage("That spot is already taken.")
            return
        self.current_tiles[space] = self.get_num(handle)
        temp_render = render
        temp = 0
        while '{}' in temp_render:
            temp_render = temp_render.replace('{}', str(self.get_type_mark(self.current_tiles[temp])), 1)
            temp += 1
            if temp >= 9:
                break
        self.chat.SendMessage(temp_render)
        if -1 not in self.current_tiles:
            self.chat.SendMessage("All tiles filled, the game is a tie!")
            return True
        winner = self.get_winner()
        if winner is not None:
            self.chat.SendMessage("{} wins!".format(self.get_user_from_mark(winner)))
            return True
        if handle == self.partner:
            self.move = self.user
        elif handle == self.user:
            self.move = self.partner
        self.chat.SendMessage("It is now {}'s turn.".format(self.move))

    @staticmethod
    def get_type_mark(num):
        if num == -1:
            return "  "
        elif num == 0:
            return "O"
        elif num == 1:
            return "X"

    def get_mark(self, handle):
        if handle == self.user:
            return "X"
        else:
            return "O"

    def get_user_from_mark(self, mark):
        if mark == "X":
            return self.user
        else:
            return self.partner

    def get_num(self, handle):
        if handle == self.user:
            return 1
        else:
            return 0

    def get_space(self, column, row):
        if row not in self.rows or column not in self.columns:
            return None
        current_row = self.rows.index(row)
        current_column = self.columns.index(column)
        if current_row == 0:
            return current_column
        else:
            return current_row * 3 + current_column

    def get_winner(self):
        counter = 0
        row_one = [self.current_tiles[0], self.current_tiles[1], self.current_tiles[2]]
        row_two = [self.current_tiles[3], self.current_tiles[4], self.current_tiles[5]]
        row_three = [self.current_tiles[6], self.current_tiles[7], self.current_tiles[8]]
        rows = [row_one, row_two, row_three]
        for row in rows:
            for num in row:
                if num == 0 and counter >= 0:
                    counter += 1
                    if counter == 3:
                        return num
                if num == 0 and counter < 0:
                    counter = 0
                if num == 1 and counter <= 0:
                    counter -= 1
                    if counter == -3:
                        return num
                if num == 1 and counter > 0:
                    counter = 0
                if num == -1:
                    counter == 0
        return None