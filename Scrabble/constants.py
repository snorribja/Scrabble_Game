from termcolor import colored
import string

BOARD_SIZE = 15
DOUBLE_LETTER_CELLS = [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12), (7, 3), (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)]
TRIPLE_LETTER_CELLS = [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)]
DOUBLE_WORD_CELLS = [(1, 1), (2, 2), (3, 3), (4, 4), (10, 10), (11, 11), (12, 12), (13, 13), (1, 13), (2, 12), (3, 11), (4, 10), (10, 4), (11, 3), (12, 2), (13, 1)]
TRIPLE_WORD_CELLS = [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)]
MIDDLE = [(7, 7)]

MENU_ASCII = '      __  ___                \n     /  |/  /__  ____  __  __\n    / /|_/ / _ \/ __ \/ / / /\n   / /  / /  __/ / / / /_/ / \n  /_/  /_/\___/_/ /_/\__,_/  \n                             '

NUMBERS_TOP = [" " + str(i) if i < 10 else str(i) for i in range(1,16)]
LETTERS_SIDE = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
SCRABBLE_BOARD_MULTIS = [colored('T W', "red",attrs=['bold']),colored('D W', "blue",attrs=['bold']),colored('T L', "magenta",attrs=['bold']),colored('D L',"light_cyan",attrs=['bold']),colored(' ✯ ', "yellow",attrs=['blink'])]


ALPHABET = list(string.ascii_uppercase)

LETTER_MULTI_DICT = {colored('T W', "red",attrs=['bold']): 1 ,colored('D W', "blue",attrs=['bold']): 1, colored('T L', "magenta",attrs=['bold']): 3 , colored('D L',"light_cyan",attrs=['bold']): 2 , colored(' ✯ ', "yellow",attrs=['blink']): 1 , ' ': 1, 'A': 1, 'B': 1, 'C': 1, 'D': 1, 'E': 1, 'F': 1, 'G': 1, 'H': 1, 'I': 1, 'J': 1, 'K': 1, 'L': 1, 'M': 1, 'N': 1, 'O': 1, 'P': 1, 'Q': 1, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 1, 'W': 1, 'X': 1, 'Y': 1, 'Z': 1}
WORD_MULTI_DICT = {colored('T W', "red",attrs=['bold']): 3 , colored('D W', "blue",attrs=['bold']): 2 , colored('T L', "magenta",attrs=['bold']): 1 , colored('D L',"light_cyan",attrs=['bold']): 1 , colored(' ✯ ', "yellow",attrs=['blink']): 2 , ' ': 1, 'A': 1, 'B': 1, 'C': 1, 'D': 1, 'E': 1, 'F': 1, 'G': 1, 'H': 1, 'I': 1, 'J': 1, 'K': 1, 'L': 1, 'M': 1, 'N': 1, 'O': 1, 'P': 1, 'Q': 1, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 1, 'W': 1, 'X': 1, 'Y': 1, 'Z': 1}

ILLEGAL_POS = [-1, 15]