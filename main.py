from tkinter import *
from itertools import cycle
from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BoardSize = 3
DefaultPlayers = (Player(label="X", color="red"), Player(label="O", color="lightblue"))

class TicTacToeGame:
    def __init__(self, players=DefaultPlayers, board_size=BoardSize):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [[Move(row, col) for col in range(self.board_size)] for row in range(self.board_size)]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [[(move.row, move.col) for move in row] for row in self._current_moves]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def is_valid_move(self, move):
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        return self._has_winner

    def is_tied(self):
        no_winner = not self._has_winner
        played_moves = (move.label for row in self._current_moves for move in row)
        return no_winner and all(played_moves)

    def toggle_player(self):
        self.current_player = next(self._players)

    def reset_game(self):
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

class TicTacToeBoard(Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = Menu(master = self)
        self.config(menu = menu_bar)
        file_menu = Menu(master = menu_bar, tearoff = False)
        file_menu.add_command(label="Play Again", command = self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label = "Exit", command = quit)
        menu_bar.add_cascade(label = "File", menu = file_menu)

    def _create_board_display(self):
        display_frame = Frame(master=self)
        display_frame.pack(fill=X)
        self.display = Label(master=display_frame, text="TIC-TAC-TOE", font=("Arial", 24, "bold"))
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=35)
            self.columnconfigure(row, weight=1, minsize=50)
            for col in range(self._game.board_size):
                button = Button(master=grid_frame, text="", font=("Arial", 44, "bold"), fg="black", width=3, height=2, relief="ridge", bd=10, bg="#323535")
                self._cells[button] = (row, col)
                button.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
                button.bind("<Button-1>", self.play)

    def play(self, event):
        clicked_button = event.widget
        row, col = self._cells[clicked_button]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_button)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="green")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f"Player {self._game.current_player.label} won!"
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _update_button(self, clicked_button):
        clicked_button.config(text=self._game.current_player.label)
        clicked_button.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color=None):
        if color is None:
            color = self._game.current_player.color
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="black")

    def reset_board(self):
        self._game.reset_game()
        self._update_display(msg="TIC-TAC-TOE", color= "black")
        for button in self._cells.keys():
            button.config(highlightbackground="red")
            button.config(text="")
            button.config(fg="black")

def main():
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()