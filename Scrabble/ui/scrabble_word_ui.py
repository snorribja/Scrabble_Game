from logic.scrabble_word_logic import ScrabbleWordLogic
from termcolor import colored

class ScrabbleWordUI:
    def __init__(self):
        self.logic = ScrabbleWordLogic()

    def word_checker(self):
        """
        Asks the user to enter a word and checks if it is a valid word in Scrabble.
        Uses the is_word_valid() method from the ScrabbleLogic class to check the validity of the word.
        Prints a message indicating whether the word is valid or not.
        """
        word = input('Enter the word that you want to check: ')
        if self.logic.is_word_valid(word):
            is_valid = colored("is", color='green')
            print(f'{word[0].upper()}{word[1:]} {is_valid} a valid word in Scrabble!')
        else:
            is_not = colored("is NOT",color='red')
            print(f'{word[0].upper()}{word[1:]} {is_not} a valid word in Scrabble!')

    def add_word(self):
        """
        Asks the user to enter a word and adds it to the set of valid words in the ScrabbleLogic class.
        Uses the add_word() method from the ScrabbleLogic class to add the word.
        """
        word = input('Enter the word that you want to add: ')
        self.logic.add_word(word)
        print(f'{word} has been added to your Scrabble game!')


        
            