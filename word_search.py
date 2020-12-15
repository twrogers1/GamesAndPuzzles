class Puzzle():
    def __init__(self, grid: str, word_bank: list):
        self.grid = self._make_board(grid)
        self.bank = word_bank
        self.counter = 0 # count of checked words
        self.found_coords = [] # (y,x) coordinates for cells contained in found words
    

    def __str__(self):
        grid = self.grid.copy()
        
        # set font weight for each character
        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                if (y,x) in self.found_coords:
                    char = "\033[1m" + "\033[3m" + char.upper() + "\033[0m" # bold, italics, upper
                else:
                    char = "\033[2m" + char.lower() + "\033[0m" # light, lower
                grid[y][x] = char
                
        string = ""
        for row in grid:
            border = "-" * (len(row)*4) + "-"
            string += border
            string += "\n"
            string += "| " + " | ".join(row) + " |"
            string += "\n"
        string += border
        string += "\n\nWord Bank:\n"
        string += "- " + "\n- ".join(self.bank)
        string += "\n"
        return string


    def _make_board(self, grid_str):
        """ Take in the :grid_str: to create a 2-d list of lists """
        grid = []
        for row in grid_str.splitlines():
            row = row.strip().upper()
            if row == "":
                continue
            grid.append(list(row))

        return grid


    def _points_between_two_coords(self, c1: tuple, c2: tuple):
        """ Find the points including and between the two given (y,x) coordinates """
        y1,x1 = c1
        y2,x2 = c2
        
        y_diff = 0 if y1-y2 == 0 else 1
        x_diff = 0 if x1-x2 == 0 else 1
        
        coords = []
        while True:
            if (y1,x1) > (y2,x2):
                break
            coords.append((y1,x1))
            x1 += x_diff
            y1 += y_diff

        self.found_coords.extend(coords)


    def _look_coord(self, y,x):
        """
        Look at the given y,x coordinate for its character
        coord 0,0 refers to the top-left of the grid
        As y increases, move down
        As x increases, move right
        If the coord is out of bounds, return None
        """
        if y < 0 or x < 0:
            return None
        try:
            return self.grid[y][x]
        except IndexError: # index has moved out of bounds
            return None
    

    def _reverse(self, string: str):
        """ Reverse the given :string: """
        return string[::-1]


    def _check_word(self, word):
        """ Check if the given word is in the word bank. If yes, return the word, else return False """
        bank = [b.upper() for b in self.bank]
        word = word.upper()
        self.counter += 1
        if word in bank:
            return word
        elif self._reverse(word) in bank:
            return self._reverse(word)
        else:
            return False


    def _scan(self, y,x, deltay, deltax):
        """ 
        Scan the grid in the specified direction.
        y,x is the starting coordinate in the grid
        deltay, deltax are how many to increment for each scan. 
            e.g. to scan right, pass deltay 0, deltax 1
            e.g. scan up-right, pass deltay -1, deltax 1
        At each step along the way, continue building the possible word string and check if it's valid against the word-bank.
        Return any words that are found.
        """
        found = []
        word = ""
        look_y, look_x = y,x
        while True:
            char = self._look_coord(look_y, look_x)
            if char is None:
                break
            word += char
            found_word = self._check_word(word)
            if found_word:
                found.append(tuple([found_word, (x,y), (look_x, look_y)])) # the only place we use x,y instead of y,x as this will eventually be seen by the user
                self._points_between_two_coords((y, x), (look_y, look_x))
            look_y += deltay
            look_x += deltax
        return found
         

    def solve(self):
        """ Search character-by-character to find words. """
        found = []
        for y, row in enumerate(self.grid):
            for x, _ in enumerate(row):
                # we only need to scan in these 4 directions
                # during the _check, the reverse string is searched which should account for the other 4 directions.
                scans = [
                    (0,1), # right
                    (1,0), # down
                    (1,1), # down-right
                    (-1,1) # up-right
                ]
                for deltay, deltax in scans:
                    found.extend(self._scan(y,x, deltay,deltax))
    
        found_string_parts = []
        found_string_parts.append(f"Found {len(found)} words in {self.counter*2:,} searches:")
        for f in found:
            word, start, end = f
            found_string_parts.append(f"- {word} found between ({start[0]+1},{start[1]+1}) and ({end[0]+1},{end[1]+1}).")
        found_string_parts.append("* Coordinates start in the top-left corner! The first letter is (x=1,y=1)")
        found_string_parts.append("* As x increases, move right. As y increases, move down.")
        
        found_string = "\n".join(found_string_parts)
        return found_string


if __name__ == "__main__":
    grid = """
    JSOLUTIS
    SUNARUUA
    NEPTUNET
    SONIEISU
    RCEVTRER
    AHTRAESN
    MMERCURY
    """
    word_bank = [w.strip() for w in """
    Earth
    Jupiter
    Mars
    Mercury
    Neptune
    Saturn
    Uranus
    Venus
    """.split("\n") if w.strip() != ""]
    
    p = Puzzle(grid, word_bank)
    
    found = p.solve()
    print(p)
    print(found)
