from ui.play_scrabble import Play_Scrabble
from ui.help import Help
from ui.scrabble_word_ui import ScrabbleWordUI
import tabulate as tb
from tabulate import tabulate
from constants import *
tb.PRESERVE_WHITESPACE = True



class Menu:
    def __init__(self):
        pass

    def input_prompt(self):
        while True:
            main_menu = [["1 - Play a game of Scrabble"],["2 - Check if word is valid"],["3 - Add word as a valid word"] ,["4 - Help"]]
            print(tabulate(main_menu, headers=[MENU_ASCII], tablefmt="mixed_grid"))
            command = input("Enter your command: ")
            if command.lower() == 'q':
                quit()
            elif command == "1":
                Play_Scrabble().game_of_scrabble()
            elif command == "2":
                ScrabbleWordUI().word_checker()
            elif command == "3":
                ScrabbleWordUI().add_word()
            elif command == "4":
                Help().with_commands()
            else:
                print("Invalid command! Try again.")
            

