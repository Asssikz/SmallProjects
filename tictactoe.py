class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.previous_player = 'O'
        self.current_player = 'X'

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def make_move(self, row, col):
        '''
        Makes a move on the board.
        '''
        if row < 0 or row > 2 or col < 0 or col > 2:
            print("Invalid move, try again.")
            return
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.previous_player = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        else:
            print("Cell is already taken, try again.")

    def check_win(self):
        '''
        Checks if the current player has won the game.
        '''
        diag_count_d2u = 0
        diag_count_u2d = 0
        for i in range(3):
            row_count = 0
            col_count = 0
            for j in range(3):
                if self.board[i][j] == self.previous_player:
                    row_count += 1
                if self.board[j][i] == self.previous_player:
                    col_count += 1
            if self.board[i][i] == self.previous_player:
                diag_count_d2u += 1
            if self.board[i][2 - i] == self.previous_player:
                diag_count_u2d += 1

            if row_count == 3 or col_count == 3 or diag_count_d2u == 3 or diag_count_u2d == 3:
                return True
        return False

    def check_draw(self):
        '''
        Checks if the game is a draw.
        '''
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def clear_board(self):
        '''
        Clears the board.
        '''
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def play(self):
        while True:
            self.print_board()
            row = int(input("Enter the row number (0, 1, 2): "))
            col = int(input("Enter the column number (0, 1, 2): "))
            self.make_move(row, col)
            if self.check_win():
                print(f"Player {self.previous_player} wins!")
                break
            if self.check_draw():
                print("It's a draw!")
                break

game = TicTacToe()
game.play()