"""The game Hangman! Run in console"""

import random
from string import ascii_uppercase
from time import sleep


class Hangman:
    def __init__(self, completed_words: list = None):
        self.completed_words = completed_words
        self.LIST_OF_WORDS = ["SUBTERFUGE", "SCENARIO", "GEOGRAPHY", "FREEDOM", "DECEPTION",
                              "LOLIPOP", "AVID", "XYLOPHONE", "FRIZZY", "TECHNO"]
        self.incomplete_word = ""
        self.all_guesses = []
        self.correct_guesses = []
        self.incorrect_guesses = []
        self.MAX_INCORRECT = 7
        self.ALL_BODY_PARTS = ["O", "/", "|", "\\", "|", "/", "\\"]
        self.added_body_parts = [" " for i in range(len(self.ALL_BODY_PARTS))]
        self.hangman_image = "  ____  \n  |   |  \n  |   {}  \n  |  {}{}{} \n  |   {}  \n  |  {} {} \n__|__"

    def main_loop(self):
        """Here is where the game starts and the main I/O happens"""
        # First, if the user replaying the game, remove previously guessed words
        if self.completed_words is not None:
            for word in self.completed_words:
                self.LIST_OF_WORDS.remove(word)
        # If the user manages to guess all the words in the game, quit
        if len(self.LIST_OF_WORDS) == 0:
            print("You've guessed every single word!")
            print("Thanks for playing!\nBye!")
            return None

        # Assign a word for guessing
        secret_word = random.choice(self.LIST_OF_WORDS)
        # Create a starred word to represent the secret word
        for letter in secret_word:
            self.incomplete_word += '*'

        # Start the real game play
        self.show_image_and_word()
        print(f"The secret word is {len(secret_word)} letters long.")
        while True:
            guess = input("Enter a guess between A-Z: ")
            guess = guess.upper()
            # Make sure the guess is valid
            if not self.check_guess(guess):
                continue
            else:
                self.all_guesses.append(guess)
                if guess in secret_word:
                    # The guess is correct!
                    print(f"'{guess}' is in the word!")
                    self.correct_guesses.append(guess)
                    self.add_letter_to_word(secret_word, guess)
                    self.show_image_and_word()
                else:
                    # The guess is not correct
                    print(f"'{guess}' is not in the word.")
                    self.incorrect_guesses.append(guess)
                    self.show_image_and_word(guess)
                    print(f"Incorrect guesses: {self.incorrect_guesses}")
                print(f"Total guesses: {len(self.all_guesses)}\tCorrect: {len(self.correct_guesses)}\tIncorrect: {len(self.incorrect_guesses)}")
                # Check to see if the game is finished
                if self.is_finished(secret_word):
                    break

        ask_to_play_again(secret_word)

    def check_guess(self, guess: str) -> bool:
        """Make sure the entry is an alphabetic letter and nothing else"""
        if guess == "" or guess not in ascii_uppercase:
            print("Invalid guess. Try again")
            return False
        if guess in self.all_guesses:
            print("You already guessed that! Try again")
            return False
        return True

    def show_image_and_word(self, guess: str = None):
        """Show the hangman with updated body parts and the word with all correctly guessed letters showing"""
        if guess is not None:
            index = len(self.incorrect_guesses)-1
            self.added_body_parts[index] = self.ALL_BODY_PARTS[index]
        print(self.hangman_image.format(*self.added_body_parts))
        print(self.incomplete_word)

    def add_letter_to_word(self, secret_word: str, guess: str):
        """Update the displayed word with the correct letters in the correct places"""
        for i, letter in enumerate(secret_word):
            if letter.upper() == guess:
                self.incomplete_word = self.incomplete_word[:i] + guess + self.incomplete_word[i+1:]

    def is_finished(self, secret_word: str) -> bool:
        """Check to see if the word is completely guessed or if the user guessed incorrectly too many times"""
        if self.incomplete_word == secret_word:
            print("You won!")
            print(f"That took you {len(self.all_guesses)} guesses!")
            return True
        elif len(self.incorrect_guesses) == self.MAX_INCORRECT:
            print("You lost! That man has been hanged.")
            return True
        else:
            return False


def ask_to_play_again(used_word: str):
    """
    Asks user if they want to play again

    If yes, restart game without the previously guessed word as a viable option
    If no, say thanks and goodbye and quit
    If neither, ask user again
    """
    global game
    answer = input("Play again? (y/n): ")
    if answer == 'y':
        del game
        used_words.append(used_word)
        game = Hangman(used_words)
        game.main_loop()
    elif answer == 'n':
        print("Thanks for playing!\nBye!")
        del game
    else:
        print("I didn't understand your answer")
        ask_to_play_again(used_word)


if __name__ == '__main__':
    print("Welcome to Hangman!")
    sleep(1)
    used_words = []  # List to hold all previously guessed words
    game = Hangman()
    game.main_loop()
