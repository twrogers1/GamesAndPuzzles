import re 

class SudokuBoard():
    def __init__(self, board):
        """ 
        Initiliaze with a list of lists, where each sublist 
        """
        self.board = board
        self.valid = self.is_board_valid()
        if not self.valid:
            print("!! Given board is not valid")

    
    def __str__(self):
        return self._print_board()
    

    def _print_board(self):
        """ An internal method used for board printing """
        parts = ["\n"]
        for i, row in enumerate(layout):
            if i % 3 == 0 and i > 0:
                parts += "  "+ "-"*31 + "\n"
            row_string = "".join([str(r) for r in row])
            re_row = re.compile(r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)")
            parts += re_row.sub("  \\1  \\2  \\3  |  \\4  \\5  \\6  |  \\7  \\8  \\9  \n", row_string)
        return "".join(parts)


    def is_board_valid(self):
        """ Determines if the given board is valid by checking the dimensions """
        row_count = len(self.board)
        column_count = len([len(row) for row in self.board if len(row) == 9])
        return True if row_count == 9 and column_count == 9 else False


    def find_next_empty(self):
        """
        Find the next empty space on the board. Works from left-to-right, top-to-bottom.
        Returns a coordinate - a tuple of index positions: <row, col>. If no empty positions are found, returns None, None.
        """
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return row, col
        
        return None, None


    def is_guess_valid(self, row, col, guess):
        """
        Perform a check for the given (row,col) and guess. If the guess *could* be valid (i.e. it doesn't break the constraints of sudoku), returns True.
        """
        # check row
        board_row = self.board[row]
        if guess in board_row:
            return False
        
        # check column
        board_column = []
        for c in range(9):
            board_column.append(self.board[c][col])
        if guess in board_column:
            return False
        
        # check subgrid
        board_subgrid = []
        subgrid_startpos_x = row // 3 * 3
        subgrid_startpos_y = col // 3 * 3
        for row in range(subgrid_startpos_x, subgrid_startpos_x+3):
            for col in range(subgrid_startpos_y, subgrid_startpos_y+3):
                board_subgrid.append(self.board[row][col])
        if guess in board_subgrid:
            return False
        
        return True


    def solve(self):
        """
        Solve the board.
        Start by finding the next empty spot iterating through guesses 1-9. If a guess would be a valid entry, place it on the board and recurse.
        If a guess would break the board, set the value to 0, to allow for backtracking.
        Once there are no more empty spaces, return
        """
        row, col = self.find_next_empty()
        if row is None:
            return True
        
        for guess in range(1,10):
            if self.is_guess_valid(row, col, guess):
                self.board[row][col] = guess
                if self.solve():
                    return True
            self.board[row][col] = 0



if __name__ == "__main__":
    layout = [
        [3,6,2,1,4,5,7,0,0],
        [0,4,0,0,0,0,6,3,0],
        [0,0,8,0,0,0,0,0,0],
        [5,0,0,0,0,2,0,7,3],
        [0,2,3,0,7,0,5,9,0],
        [7,9,0,4,0,0,0,0,1],
        [0,0,0,0,0,0,2,0,0],
        [0,3,4,0,0,0,0,1,0],
        [0,0,5,9,2,4,3,6,7],
    ]
    board = SudokuBoard(layout)
    print("Original:\n", board)
    board.solve()
    print("Solved:\n", board)
