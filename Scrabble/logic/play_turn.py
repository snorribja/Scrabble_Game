from logic.scrabble_bag import ScrabbleBag
from constants import *
from logic.legal_pos_and_dir import LegalPosition 
from logic.legal_players import * 


class PlayTurn:
    def __init__(self, scrabbleboard):
        self.scrabbleboard = scrabbleboard
        self.pass_turn_counter = 0
        self.scrabble_bag = ScrabbleBag()
        self.multi_counter = list()
        self.player_names = []
        self.player_turn_index = 0
        self.players_dict = dict()
        self.legal_pos = LegalPosition()
        

    def place_word(self, word: str, direction: str, start_pos: tuple) -> None:
        """Place a word on the board starting at the given position in the given direction.

        Args:
            word (str): The word to be placed on the board.
            direction (str): The direction in which the word is to be placed, either 'H' for horizontal or 'V' for vertical.
            start_pos (tuple): The starting position for the word placement in (row, column) format.

        Returns:
            None
        """
        # Reset pass turn counter
        self.pass_turn_counter = 0

        # Extract starting row and column positions
        row, col = start_pos

        # Place letters on board
        for i, letter in enumerate(word):
            if direction == 'V':
                # Place letter vertically
                self[row + i, col] = f'{letter.upper()}'
            elif direction == 'H':
                # Place letter horizontally
                self[row, col + i] = f'{letter.upper()}'



    def get_multi_counter(self, word, direction, start_pos):
        """
        Get the multipliers for each letter in the given word, based on the multipliers on the board.

        Args:
            word (str): The word to place on the board.
            direction (str): The direction of the word, either 'H' for horizontal or 'V' for vertical.
            start_pos (tuple): The starting position of the word as a tuple (row, column).

        Returns:
            None
        """
        # Reset the multi_counter list
        self.multi_counter = list()

        # Get the starting row and column
        row, col = start_pos

        # Iterate over each letter in the word
        for i in range(len(word)):
            # Determine the position of the current letter based on the word direction
            if direction == 'V':
                current_pos = (row+i, col)
            if direction == 'H':
                current_pos = (row, col+i)
            
            # Add the multiplier at the current position to the multi_counter list
            self.multi_counter.append(self[current_pos])



    def allow_to_place(self, word, direction, start_pos):
        """Checks if a given word can be placed in a given direction starting from a given position.

        Args:
            word (str): The word to be placed.
            direction (str): The direction in which to place the word ('H' for horizontal, 'V' for vertical).
            start_pos (tuple): The position on the board where the first letter of the word should be placed.

        Returns:
            bool: True if the word can be placed in the given direction starting from the given position, False otherwise.
        """

        row, col = start_pos
        bool_list = list()

        # Check if each letter in the word can be placed in the given direction starting from the given position
        for i, j in enumerate(word):
            if direction == 'V':
                bool_list.append(self[row+i,col] == j or self[row+i,col] == " " or self[row+i,col] in SCRABBLE_BOARD_MULTIS)
            if direction == 'H':
                bool_list.append(self[row,col+i] == j or self[row,col+i] == " " or self[row,col+i] in SCRABBLE_BOARD_MULTIS)

        # Check if the word touches any other existing words on the board
        return all(bool_list) and self.legal_pos.valid_words_touching(word, direction, start_pos, self.scrabbleboard)
                

    def add_points_for_word(self, word):
        """
        Calculates the points obtained by the current player for placing a word on the board.

        Args:
            word (str): The word placed on the board.

        Returns:
            None

        Raises:
            None
        """
        # Initialize points counter
        points = 0
        
        # Calculate points for each letter in the word based on letter and word multipliers
        for letter, multi in zip(word, self.multi_counter):
            points += self.scrabble_bag.letter_values[letter] * LETTER_MULTI_DICT[multi]
        
        # Calculate points for the entire word based on word multipliers
        for multi_word in self.multi_counter:
            points *= WORD_MULTI_DICT[multi_word]
        
        # Add points to the current player's score
        self.players_dict[self.player_turn][1] += points

    
    def add_points_for_perpendicular_words(self, word, direction, pos, on_hand):
        """
        Adds points for perpendicular words formed by placing the given word at the given position and direction.

        Parameters:
        word (str): The word being placed.
        direction (str): The direction of the word placement (either 'H' for horizontal or 'V' for vertical).
        pos (tuple): The position of the first letter of the word on the board (row, column).
        on_hand (list): The list of letters on hand.

        Returns:
        None.
        """
        # Get the list of tuples containing perpendicular words and their start positions
        perpendicular_tuples = self.legal_pos.get_perpendicular_word_list(word, direction, pos, self.scrabbleboard)
        # Iterate through the list of on-hand letters
        for i, your_letter in enumerate(on_hand):
            # Only process non-empty letters and if there is a perpendicular word at this position
            if your_letter and perpendicular_tuples[i]:
                points = 0
                perpen_word, start_pos = perpendicular_tuples[i]
                # Get the multipliers for each letter in the perpendicular word
                self.get_multi_counter(word, direction, start_pos)
                # Calculate the points for the perpendicular word
                for letter, multi in zip(perpen_word, self.multi_counter):
                    points += self.scrabble_bag.letter_values[letter] * LETTER_MULTI_DICT[multi]
                for multi_word in self.multi_counter:
                    points *= WORD_MULTI_DICT[multi_word]
                # Add the points to the current player's score
                self.players_dict[self.player_turn][1] += points

    def swap_letters(self, letter_to_swap):
        """
        Swaps the specified letters with new tiles drawn from the scrabble bag.
        
        Args:
        - letter_to_swap (str): A string of letters to be swapped from the player's hand.
        
        Returns:
        - None
        """
        # Reset pass turn counter
        self.pass_turn_counter = 0
        
        # Get number of new tiles to draw
        number_of_new_tiles = len(letter_to_swap)
        
        # Remove swapped tiles from player's hand
        self.remove_tiles_from_hand(letter_to_swap)
        
        # Draw new tiles from the scrabble bag
        new_tiles = self.scrabble_bag.draw_tiles(letter_to_swap, number_of_new_tiles)
        
        # Add new tiles to player's hand
        for new in new_tiles:
            self.players_dict[self.player_turn][0].append(new)


    def remove_tiles_from_hand(self, letter_to_swap):
        """
        Removes specified letters from the player's hand.
        
        Args:
        - letter_to_swap (str): A string of letters to be removed from the player's hand.
        
        Returns:
        - None
        """
        # Remove specified letters from player's hand
        for letter in letter_to_swap:
            if letter in self.players_dict[self.player_turn][0]:
                self.players_dict[self.player_turn][0].remove(letter)


    def pass_turn(self):
        """
        Increases the pass turn counter to indicate that the player has passed their turn.
        
        Args:
        - None
        
        Returns:
        - None
        """
        # Increase pass turn counter
        self.pass_turn_counter += 1


    def add_to_hand(self, word, direction, pos):
        """
        Adds the given word to the player's hand, removing the corresponding tiles and updating the score.
        
        Parameters:
            - word (str): the word to add to the player's hand.
            - direction (str): the direction in which the word is placed ('H' for horizontal or 'V' for vertical).
            - pos (tuple of int): the starting position of the word on the board, as a tuple of (row, column).
            - on_hand (list of str): the tiles currently in the player's hand.
            
        Returns:
            None
        """
        # Update multipliers for the placed word
        self.get_multi_counter(word, direction, pos)
        
        # Add points for the placed word
        self.add_points_for_word(word)

        on_hand = self.legal_pos.use_of_your_letters(word, direction, pos, self.scrabbleboard)
        
        # Add points for perpendicular words (if any)
        self.add_points_for_perpendicular_words(word, direction, pos, on_hand)
        
        # Remove tiles from hand
        self.remove_tiles_from_hand(word)
        
        # Check if all 7 tiles were used and add corresponding points
        used_letters = 7 - len(self.players_dict[self.player_turn][0])
        if used_letters == 7:
            self.add_points_for_using_all_7_tiles()
        
        # Draw new tiles from the bag and add them to the player's hand
        new_letters = self.scrabble_bag.draw_tiles(None, used_letters)
        for i in new_letters:
            self.players_dict[self.player_turn][0].append(i)
        
       
        

    def add_points_for_using_all_7_tiles(self):
        """
        Adds 50 points to the current player's score if they have used all 7 of their tiles in a single turn.
        """
        self.players_dict[self.player_turn][1] += 50


    def change_turn(self):
        """
        Changes the current player turn to the next player in the list of player names.
        """
        self.player_turn_index = (self.player_turn_index + 1) % len(self.player_names)
        self.player_turn = self.player_names[self.player_turn_index]


    def __getitem__(self, pos):
        """
        Returns the value at the given position in the Scrabble board.
        """
        return self.scrabbleboard[pos[0]][pos[1]]


    def __setitem__(self, pos, letter):
        """
        Sets the value at the given position in the Scrabble board to the given letter.
        """
        self.scrabbleboard[pos[0]][pos[1]] = letter
