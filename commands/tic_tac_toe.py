from util.plugin import command


render = "   1 2 3 \nA |{}|{}|{}|\n----------\nB |{}|{}|{}|\n----------\nC |{}|{}|{}|"

# !ttt start josh0309
# !ttt move a3
# !ttt quit
games = []


@command(name='ttt')
def tic_tac_toe(chat, message, args, sender):
    if len(args) == 0:
        chat.SendMessage("Provide an argument.")
        return
    if args[0] == "start":
        if len(args) != 2:
            chat.SendMessage("Provide a partner.")
            return
        game = TicTacToe(chat, sender.Handle, args[1])
        games.append(game)
        chat.SendMessage("Started game.")
    elif args[0] == "end":
        get_game_by_sender(chat, sender.Handle).end_game()
    elif args[0] == "move":
        if len(args) != 2:
            chat.SendMessage("Provide a column and row.")
            return
        if len(args[1]) != 2:
            chat.SendMessage("Provide a row and column in a single argument. eg. e3")
            return
        move = args[1]
        game = get_game_by_sender(chat, sender.Handle)
        if game is None:
            chat.SendMessage("You do not have a running game.")
            return
        game.make_move(sender.Handle, move[1], move[0])


def get_game_by_sender(chat, sender):
    for game in games:
        if (game.user == sender or game.partner == sender) and chat == game.chat:
            return game


class TicTacToe:
    rows = ['a', 'b', 'c']
    columns = ['1', '2', '3']
    current_tiles = [-1, -1, -1,
                     -1, -1, -1,
                     -1, -1, -1]

    def __init__(self, chat, user, partner):
        self.chat = chat
        self.user = user
        self.partner = partner
        self.move = partner

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
            self.end_game()
            return
        winner = self.get_winner()
        if winner is not None:
            self.chat.SendMessage("The letter {} wins!".format(self.get_type_mark(winner)))
            self.end_game()
            return
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

    def end_game(self):
        games.remove(self)

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
        for num in self.current_tiles:
            if num == 0 and counter >= 0:
                counter += 1
                if counter == 4:
                    return num
            if num == 0 and counter < 0:
                counter = 0
            if num == 1 and counter <= 0:
                counter -= 1
                if counter == -4:
                    return num
            if num == 1 and counter > 0:
                counter = 0
            if num == -1:
                counter == 0
        return None