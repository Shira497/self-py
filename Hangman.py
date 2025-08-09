"""
This program runs the game of Hangman.
The user enters a secret word, and then tries to guess the letters
For each guess, the program indicates whether it is correct or not,
and displays a graphical representation
of the player's progress based on the number of incorrect guesses.
"""

HANGMAN_PICS = [
    "x-------x",
    """    x-------x
    |
    |
    |
    |
    |""",
    """    x-------x
    |       |
    |       0
    |
    |
    |""",
    """    x-------x
    |       |
    |       0
    |       |
    |
    |""",
    """    x-------x
    |       |
    |       0
    |      /|\\
    |
    |""",
    """    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |""",
    """    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |""",
]


def check_valid_input(letter_guessed: str, old_letters_guessed: str):
    """
    Checks if the guessed letter is valid:
    - Only one character
    - Alphabetic character
    - Not guessed before

    Parameters:
    letter_guessed (str): The guessed letter.
    old_letters_guessed (list): List of previously guessed letters.

    Returns:
    bool: True if valid, False otherwise.
    """
    return (
        len(letter_guessed) == 1
        and letter_guessed.isalpha()
        and letter_guessed.lower() not in old_letters_guessed
    )


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    Updates the list of guessed letters if the input is valid.
    Prints error message and the list of guessed letters if invalid.

    Parameters:
    letter_guessed (str): The guessed letter.
    old_letters_guessed (list): List of previously guessed letters.

    Returns:
    bool: True if the letter was added, False otherwise.
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed.lower())
        return True
    else:
        print("X")
        print(" <- ".join(sorted(old_letters_guessed)))
        return False


def show_hidden_word(secret_word, old_letters_guessed):
    """
    Returns a string of the guessed letters
    and underscores for missing letters.

    Parameters:
    secret_word (str): The secret word to guess.
    old_letters_guessed (list): List of guessed letters.

    Returns:
    str: The formatted string showing guessed letters and underscores.
    """
    new_str = ""
    for letter in secret_word:
        if letter in old_letters_guessed:
            new_str += letter
        else:
            new_str += "_"
    return " ".join(new_str)


def check_win(secret_word: str, old_letters_guessed: list) -> bool:
    """
    Checks if the player has guessed the entire word.

    Parameters:
    secret_word (str): The secret word.
    old_letters_guessed (list): List of guessed letters.

    Returns:
    bool: True if all letters were guessed, False otherwise.
    """
    hidden = show_hidden_word(secret_word, old_letters_guessed)
    return "_" not in hidden.replace(" ", "")


def choose_word(file_path: str, index: int) -> tuple[int, str]:
    """
    Chooses a secret word from a file based on the given index.
    Counts unique words and handles index circularly.

    Parameters:
    file_path (str): Path to the file containing words.
    index (int): The position of the chosen word (1-based).

    Returns:
    tuple: (number_of_unique_words, chosen_word)
    """
    with open(file_path, "r", encoding="utf-8") as file:
        words = file.read().split()

    unique_words = list(dict.fromkeys(words))
    num_unique_words = len(unique_words)
    circular_index = (index - 1) % num_unique_words
    chosen_word = unique_words[circular_index]

    return (num_unique_words, chosen_word)


def main():
    print("Welcome to the game Hangman")
    print(
        r"""   _    _
...    | |  | |
...    | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
...    |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \
...    | |  | | (_| | | | | (_| | | | | | | (_| | | | |
...    |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|"""
    )

    secret_word = input("Enter the secret word: ").lower()
    print("_ " * len(secret_word))

    old_letters_guessed = []
    max_mistakes = len(HANGMAN_PICS) - 1
    mistakes = 0

    while mistakes < max_mistakes:
        print(show_hidden_word(secret_word, old_letters_guessed))
        guess = input("Guess a letter: ")

        if try_update_letter_guessed(guess, old_letters_guessed):
            if guess.lower() not in secret_word:
                mistakes += 1
                print(
                    "Wrong guess! You have "
                    + str(max_mistakes - mistakes)
                    + " tries left."
                )
                print(HANGMAN_PICS[mistakes])
            else:
                print("Good guess!")

            if check_win(secret_word, old_letters_guessed):
                print(f"Congratulations! You guessed the word: {secret_word}")
                break
        else:
            print("Invalid input or letter already guessed.")

    if not check_win(secret_word, old_letters_guessed):
        print("Game over! The word was: " + str(secret_word))


if __name__ == "__main__":
    main()
