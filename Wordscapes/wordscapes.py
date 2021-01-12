from itertools import permutations
from collections import Counter


class Wordscapes():
    """ Simple class to provided guesses for the hidden word """
    def __init__(self, bank, word=None, found=None):
        self.bank = list(bank.upper())
        if word:
            self.word = list(word.upper())
        if found:
            self.found = [x.strip() for x in list(found.upper().split(","))]
    

    def guess(self):
        """ Create a list of 'valid' guesses in a list. """
        guesses = []
        char_indexes = dict([(i,l) for i,l in enumerate(self.word) if l != "_"])
        for p in permutations(self.bank, len(self.word)):
            guess = "".join(p)
            
            # ensure this permutation hasn't already been found
            if hasattr(self, found) and guess in self.found:
                continue
            
            # ensure this permutation has at least one vowel
            if not any(v in p for v in list("AEIOU")):
                continue

            # ensure the hard-coded characters are in place for this permutation
            skip = False
            for k,v in char_indexes.items():
                if p[k] != v:
                    skip = True
                    break
            if skip:
                continue

            guesses.append(guess)
        
        return guesses


if __name__ == "__main__":
    bank = "OIAPN" # given word bank
    word = "P_A__" # word to guess. Use _ for blanks
    found = "" # csv of words already found, optional

    WS = Wordscapes(bank, word=word)
    
    guesses = WS.guess()
    print(f"Found {len(guesses)} guesses:")
    for g in guesses:
        print("-",g)
