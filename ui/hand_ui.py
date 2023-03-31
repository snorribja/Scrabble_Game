from tabulate import tabulate
from logic.scrabble_bag import *
from termcolor import colored

class HandUI():
    def __init__(self):
        self.scrabble_bag = ScrabbleBag()
        
    def the_hand(self, player_turn, players_dict) -> str:
        value_string = ''
        for letter in players_dict[player_turn][0]:
            value_string += f'  {colored(str(self.scrabble_bag.letter_values[letter]), color="dark_grey")} '
        board_list = tabulate([players_dict[player_turn][0]], tablefmt='mixed_grid', stralign="center").split("\n")
        board_str = "\n".join([line if i % 2 == 0 else line.rstrip() for i, line in enumerate(board_list)])
        return board_str + "\n" + value_string + "\n"

        