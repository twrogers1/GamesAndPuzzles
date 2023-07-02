from pathlib import Path


def get_word_bank(file_name: str = "word_bank.txt") -> list[str]:
    """
    Read the `file_name` and return a list of words.
    
    Args:
        file_name: str for the filename of words

    Returns:
        list of strings
    """
    txt_file = Path(__file__).parent / file_name
    return [x.strip() for x in txt_file.read_text().splitlines() if x.strip()]


if __name__ == "__main__":
    words = get_word_bank()
    print(words)
