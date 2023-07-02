import random
from string import ascii_lowercase, ascii_uppercase
from turtle import Screen, Turtle

from colors import Dracula


# configs
ALPHABET = list(map(lambda x: x[0] + x[1], zip(ascii_uppercase, ascii_lowercase)))  # Aa Bb Cc
NUMBERS = list(range(1, 101))
SHUFFLE = True  # whether to shuffle up the items
SAMPLE = -1  # how many items to quiz with (use -1 for no limit)
BACKGROUND_COLOR = Dracula.Background
TEXT_COLOR = Dracula.Green


def wipe_screen(s: Screen):
    """ clear screen and set back the background color """
    s.clear()
    s.bgcolor(BACKGROUND_COLOR)


def quiz(
        s: Screen,
        t: Turtle,
        items: list[str | int],
        sample_size: int = -1,
        shuffle: bool = False,
        check_guess: bool = True
) -> None:
    """
    Use Turtle to quiz for accuracy with the given items

    Args:
        s: Screen instance
        t: Turtle instance
        items: list of items (e.g. letters / numbers)
        sample_size: the number of items to check
        shuffle: whether to shuffle the items
        check_guess: if True, ask for user input to tally correct answers
    """
    print("\n" + "-"*30)
    print(f"Testing with item bank {', '.join(map(str, items))}...")
    if shuffle:
        random.shuffle(items)
        print("- Shuffled items.")
    if sample_size > 0:
        print(f"- Sample size = {sample_size}.")
    
    correct = 0
    for i, x in enumerate(items, start=1):
        t.write(x, align="center", font=FONT)
        if check_guess:
            if isinstance(x, str) and len(x) == 2:
                correct += guess(x[0])  # assumes this is the alphabet, just use the first letter to circumvent "Aa" format
            else:
                correct += guess(x)
        wipe_screen(s)
        
        if sample_size > 0 and i >= sample_size:
            break

    if check_guess:
        print(f"\nScore: {correct} of {i} ({correct / i:1%})")
    
    return correct


def guess(answer: str | int) -> bool:
    """ Prompt the console to guess the given `answer`. Returns a bool for accuracy. """
    guess = input(f"Guess ({answer}) > ")
    correct = str(guess).lower() == str(answer).lower()
    print("✔" if correct else "❌")
    return correct


if __name__ == "__main__":
    # screen setup
    s = Screen()
    s.title("Guessing Game - ABCs & 123s")
    s.setup(width=1200, height=700)
    wipe_screen(s)  # also sets the bg color

    # turtle setup
    t = Turtle()
    t.hideturtle()
    t.penup()
    t.pencolor(TEXT_COLOR)
    font_size = 256
    # t.setx(-font_size/2)
    t.sety(-font_size/2)
    FONT = ("Times", font_size, "bold")
    
    quiz(s, t, ALPHABET, sample_size=SAMPLE, shuffle=SHUFFLE, check_guess=True)
    quiz(s, t, NUMBERS, sample_size=SAMPLE, shuffle=SHUFFLE, check_guess=True)
