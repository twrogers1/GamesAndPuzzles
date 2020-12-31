import random
import re
import time
from collections import defaultdict


class NameGame():
    __RULES__ = """
    -= N A M E   G A M E =-
    
    Rules:
    - Players take turns naming people, typically celebrities
    - The named person must have a first and last name (In other words, Seal isn't a valid choice)
    - The choice on turn 1 can be any person. In this script, it's chosen by the CPU randomly
    - For the choices on turn 2 and after, the first letter of the first name must start with the first letter of the last name from the prior choice.
        (For example, if James Bond was chosen on turn 1, Bruce Wayne would be a valid choice on turn 2, Walter White would be a valid choice on turn 3, and so on)
    - Names cannot be repeated
    - The game ends when players run out of choices

    Pro Tips:
    - Try to remember names (lelz)
    - The scope of the people bank can be expanded however you like
        - Try using fictional characters, authors, or people you know IRL

    Good luck!

    (During your turn, type 'q' or 'quit' to quit.)
    """
    def __init__(self):
        self.name_bank = self._parse_names() # word bank for the CPU player - stored in lowercase
        self.played = [] # names already played - stored in lowercase


    def __str__(self):
        """ Print an alphabetical ordering of the names in the name_bank along with the names played. """
        string = "\nRemaining Name Bank:\n"
        for k, v in sorted(list(self.name_bank.items())):
            names = [n.title() for n in sorted(v)]
            if len(names) > 0:
                string += f"{k.upper()} - {', '.join(names)}\n"

        string += "\nPlayed Names:\n"
        string += " -> ".join([p.title() for p in self.played])
        string += f"\nStreak of {len(self.played)}."
        
        return string


    def _parse_names(self):
        """ Internal method - Read in the names.txt file and parse them to a defaultdict, where the keys are the beginning letter of the first names. """
        name_bank = defaultdict(set)
        with open("names.txt", "r") as f:
            for name in f.readlines():
                name = name.strip().lower()
                if name != "":
                    letter = name[0]
                    name_bank[letter].add(name)
           
        return name_bank
    
    
    def _remove_from_bank(self, name):
        """ Internal method - Take the given :name: and remove it from self.name_bank """ 
        name = name.lower()
        letter = name[0] 
        if name in self.name_bank[letter]:
            self.name_bank[letter].remove(name.lower())

    def _choose_random_name(self, letter, remove=True):
        """ Internal method - Choose a random name from the self.name_bank (and by defualt, :remove: it) for the given :letter: """        
        letter = letter.lower()
        names = list(self.name_bank[letter])
        if len(names) > 0:
            choice = random.choice(names)
            if remove:
                self._remove_from_bank(choice)
        else:
            choice = None       
    
        return choice


    def _trim_postfix(self, name):
        """ Given a fullname :name:, parse out the common suffixes (Sr., Jr., III, etc.). Returns a name string. """
        
        def _is_suffix(part):
            """ Determine if the given name :part: is a postfix. Returns a bool. """
            # sub out all periods - as seen in "Sr."
            # compare against Sr., Jr., and roman numerals 1-10
            part = part.replace(".", "")
            # part = re.sub(r"[^\w]", "", part) # could break hyphens
            if part.lower() in ["sr", "jr"] or \
                part.upper() in "I, II, III, IV, V, VI, VII, VIII, VIX, IX, X".split(", ") or \
                part == "":
                return True
            else:
                return False

        parts = [p for p in name.split(" ") if not _is_suffix(p)]
        return " ".join(parts)


    def parse_last_name(self, name):
        """ Given a fullname :name:, parse it so the first letter of the last name is returned. """
        name = self._trim_postfix(name)
        return name.split(" ")[-1][0]


    def get_name_input(self, letter=None):
        """ Get input from the user and validate it before returning. """
        name = None
        try:
            while not name:
                prompt = f"Enter a name starting with {letter.upper()} > " if letter else "Enter a name > "
                name = input(prompt).strip()
                name = re.sub(r"\s{2,}", " ", name) # handle multiple spaces in the input

                # quit
                if name.lower() in "q, quit, stop, exit".split(", "):
                    return None
                
                # name should contain 2+, non-suffix words
                if " " not in self._trim_postfix(name):
                    print("!! Name must contain two or more words.")
                    name = None
                    continue
                
                # if a letter is specified, check that the given name starts with it
                if letter is not None and name[0].lower() != letter.lower():
                    print(f"!! Name must start with the letter {letter.upper()}.")
                    name = None
                    continue

                # name can't have been played previously
                if name.lower() in [p.lower() for p in self.played]:
                    print("!! Name was already played. Try another.")
                    name = None
                    continue
        except KeyboardInterrupt:
            return None
        
        self._remove_from_bank(name) # don't let CPU choose this name
        return name
    

    def play(self, players=1):
        """
        Play the game. A random seed will be chosen from the word bank to get things started. 
        :players=0: (or less than 1): the computer will play itself
        :players=1: play against the computer
        """
        letter = random.choice(list(self.name_bank))
        if players < 1:
            while True:
                name = self._choose_random_name(letter)    
                if name is None:
                    break # computer ran out of options.
                self.played.append(name.lower())
                letter = self.parse_last_name(name)
        elif players == 1:
            print(NameGame.__RULES__)
            your_turn = False
            while True:
                name = self.get_name_input(letter=letter) if your_turn else self._choose_random_name(letter)
                if name is None:
                    if not your_turn:
                        print("You win, the computer ran out of options.")
                    else:
                        print("\nGame over, you quit the game.")
                    break           
                else:
                    if not your_turn:
                        time.sleep(1) # create the illusion of the CPU thinking
                    print(f"{'You' if your_turn else 'CPU'} chose {name.title()}.")
                    self.played.append(name.lower())
                    letter = self.parse_last_name(name)
                    your_turn = not your_turn # flip back and forth between yours and the computer's turn    
        
        print(self)
        
            
if __name__ == "__main__":
    game = NameGame()
    game.play(players=1)
    # game.play(players=0)