from constants import *
from tabulate import tabulate
from termcolor import colored
from logic.play_turn import PlayTurn
from itertools import zip_longest

# Initialize the board with empty cells
classic_board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Mark the cells with double letter score
for row, col in DOUBLE_LETTER_CELLS:
    classic_board[row][col] = colored('D L',"light_cyan",attrs=['bold'])

# Mark the cells with triple letter score
for row, col in TRIPLE_LETTER_CELLS:
    classic_board[row][col] = colored('T L',"magenta",attrs=['bold'])


# Mark the cells with double word score
for row, col in DOUBLE_WORD_CELLS:
    classic_board[row][col] = colored('D W',"blue",attrs=['bold'])

# Mark the cells with triple word score
for row, col in TRIPLE_WORD_CELLS:
    classic_board[row][col] = colored('T W',"red",attrs=['bold'])

for row, col in MIDDLE:
    classic_board[row][col] = colored(' ✯ ',"yellow",attrs=['blink'])


class Scrabbleboard(PlayTurn):
    def __init__(self):
        super().__init__(classic_board)


    def __str__(self):
        board_str = "\n" + "    " + "    ".join(NUMBERS_TOP) + "\n"
        board_list = tabulate(self.scrabbleboard, tablefmt='mixed_grid', stralign="center").split("\n")
        side_list = ("\n\n\n\n\n\n" + self.format_player_stats() + "\n\n\n\n\n\n" + self.format_bag()).split("\n")
        for i, lines in enumerate(zip_longest(board_list, side_list, fillvalue=' '), start=1):
            if i % 2:
                board_str += "  " + lines[0] + '     ' + lines[1]
            else:
                board_str += f"{LETTERS_SIDE[int((i-1)/2)]} " + lines[0] + f" {LETTERS_SIDE[int((i-1)/2)]}" + '   ' + lines[1]
            
            board_str += "\n"
        board_str += "    " + "    ".join(NUMBERS_TOP) + "\n"
        return board_str
    

    def format_player_stats(self):
        """Formats the statistics of players into a grid."""
        player_stats = []
        for name, stats in self.players_dict.items():
            score = stats[1]
            player_stats.append([name, score])
        player_table = tabulate(player_stats, headers=["Name", "Score"], tablefmt='mixed_grid')
        return player_table
    
    def format_bag(self):
        bag_size = colored(self.scrabble_bag.tiles_left_in_bag(), color='green')
        return tabulate([[bag_size]], headers=['Tiles left in bag!'], tablefmt='mixed_grid', numalign='center')
