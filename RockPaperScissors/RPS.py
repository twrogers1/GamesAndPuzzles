import random
from enum import Enum


class Results(Enum):
    Loss = -1
    Tie = 0
    Win = 1


    def get_result(n):
        """ Given the Enum value, return the name """
        return {r.value: r.name for r in Results}.get(n)


class RPS:
    """ Rock, Paper, Scissors class. Just call Play(). """
    winners = { 
        # (key beats value)
        "Rock": "Scissors",
        "Paper": "Rock",
        "Scissors": "Paper"
    }
    choices = list(winners.keys())
    
    def __repr__(self):
        return self.choice
    

    def _pick_random(self):
        """ Randomly choose RPS (for the computer opponent) """
        return random.choice(RPS.choices)


    def _choose(self):
        """ Allow player to choose RPS """
        
        print(f"Choose an option:")
        for i,c in enumerate(RPS.choices):
            print(f" {i+1} - {c}")
        print("(Pick 1, 2, 3, or type an option.)")
        
        valid_choices = [str(i+1) for i in range(len(RPS.choices))] # generate number options
        valid_choices.extend([rps.lower() for rps in RPS.choices]) # make choices lower()

        inpt = None
        while not inpt:
            inpt = input("> ")
            if str(inpt).lower() not in valid_choices:
                print(f"Input '{inpt}' invalid. Please try again...")
                inpt = None
        
        try:
            inpt = int(inpt)-1
            self.choice = RPS.choices[inpt]
        except ValueError:
            self.choice = inpt.capitalize()


    def Play(self):
        """
        Play a game of Rock, Paper, Scissors
        Returns an int for the results to match the Results Enum:
            -1 = Loss
            0 = Tie
            1 = Win
        """
        npc_choice = self._pick_random()
        self._choose()

        if self.choice == npc_choice:
            print(f"Tie: You both chose {self.choice} =\\")
            return 0
        elif RPS.winners[self.choice] == npc_choice:
            print(f"You win: {self.choice} beats {npc_choice} =]")
            return 1
        else:
            print(f"You lose: {npc_choice} beats {self.choice} =[")
            return -1


if __name__ == "__main__":
    import time
    from collections import defaultdict
    
    score = defaultdict(int)
    rps = RPS()

    def print_scores(score: defaultdict):
        """ Print the running scores. """
        print("\nRunning score:")
        print("- Wins:", score["Win"])
        print("- Losses:", score["Loss"])
        print("- Ties:", score["Tie"])
        return
    
    try:
        while True:
            result = rps.Play()
            score[Results.get_result(result)] += 1
            print_scores (score)   
            time.sleep(3)
            print("\n\n")
    except KeyboardInterrupt:
        print("\n\nExiting. Showing final scores:")
        print_scores (score)
        exit()
