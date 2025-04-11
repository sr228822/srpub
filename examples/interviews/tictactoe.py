import copy


def is_win(cells):
    """Return true if this set of cells is a win"""
    return cells[0] != " " and len(set(cells)) == 1


def has_win(board):
    # Check each row
    for row in range(3):
        if is_win(board[row]):
            return board[row][0]

    # check each col
    for col in range(3):
        cells = [board[0][col], board[1][col], board[2][col]]
        if is_win(cells):
            return cells[0]

    # Check diags
    cells = [board[0][0], board[1][1], board[2][2]]
    if is_win(cells):
        return cells[0]
    cells = [board[0][2], board[1][1], board[2][0]]
    if is_win(cells):
        return cells[0]

    return None


class TicTacToe:
    def __init__(self):
        self.board = []
        for _ in range(3):
            self.board.append([" ", " ", " "])

    def print_board(self):
        print("-----------")
        for row in self.board:
            print("|".join(row))

    def get_user_move(self):
        while True:
            choice = input("Enter square as row,col: ")
            try:
                parts = choice.split(",")
                if len(parts) != 2:
                    print("invalid input wrong number of vals")
                    continue
                row = int(parts[0])
                col = int(parts[1])
                assert row >= 0 and row < 3
                assert col >= 0 and col < 3
                assert self.board[row][col] == " "
                return row, col
            except Exception as e:
                print(f"invalid input: {e}")
                continue

    def enter_move(self, row, col, char):
        if self.board[row][col] != " ":
            raise Exception(
                f"Invalid entry: {row},{col} already occupied: {self.board[row][col]}"
            )
        self.board[row][col] = char

    def get_computer_move(self):
        # For each cell, see if the user could win here
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    aboard = copy.deepcopy(self.board)
                    aboard[row][col] = "X"
                    if has_win(aboard):
                        return row, col

        # Choose first unoccupied cell
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    return row, col

    def play(self):
        user_turn = True
        self.print_board()
        while True:
            if user_turn:
                user_move = self.get_user_move()
                self.enter_move(user_move[0], user_move[1], "X")
            else:
                computer_move = self.get_computer_move()
                self.enter_move(computer_move[0], computer_move[1], "O")

            self.print_board()
            if winner := has_win(self.board):
                print(f"User {winner} has won!")
                break
            user_turn = not user_turn


game = TicTacToe()
game.play()
