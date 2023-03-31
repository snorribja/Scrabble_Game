from constants import *
from logic.scrabble_word_logic import ScrabbleWordLogic
import copy


class LegalPosition:
    def __init__(self):
        self.scrabble_word_logic = ScrabbleWordLogic()
    
    def is_on_board(self, pos):
        """
        Check if the position is on the board.
        """
        row, col = self.get_position(pos)
        return row >= 0 and row < 15 and col >= 0 and col < 15
    
    
    def is_first_placement(self, word, direction, pos):
        """
        Determines if this is the first placement on the board.

        Args:
        - word (str): The word being placed.
        - direction (str): The direction of the word placement ('H' or 'V').
        - pos (tuple): The starting position of the word placement in chess notation (e.g., "A1").

        Returns:
        - bool: True if the placement is the first on the board, False otherwise.
        """
        goes_over_middle = False
        for _ in range(len(word)):
            if [(pos[0], pos[1])] == MIDDLE:
                goes_over_middle = True
            if direction == 'V':
                pos = (pos[0]+1, pos[1])
            if direction == 'H':
                pos = (pos[0], pos[1]+1)
        return goes_over_middle

    
    def valid_starting_pos(self, pos):
        """Checks if a given starting position is valid.

        Args:
            pos (str): A string representing the position to check, e.g. "A1".

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        try:
            self.get_position(pos)
            return True
        except ValueError:
            return False

    
    def get_position(self, pos):
        """
        Converts a string position on the Scrabble board to its corresponding coordinates.

        Args:
            pos (str): The string position to be converted, e.g. "H8".

        Returns:
            tuple: The tuple of coordinates (row, column) corresponding to the input position.
        """
        # Get the numeric row coordinate by subtracting 1 from the integer value of the string position (excluding the column letter)
        x_pos = int(pos[1:]) - 1
        # Get the numeric column coordinate by converting the column letter to its corresponding ASCII value and subtracting 65
        # (the ASCII value of "A"), then converting back to an integer
        y_pos = ord(pos[0].upper()) - 65
        return (y_pos, x_pos)

    
    def replace_ö(self, ö: str, player_turn: str, players_dict: dict) -> dict:
        """Replaces a player's 'Ö' tile with a specified letter.

        Args:
            ö (str): The letter to replace 'Ö' with.
            player_turn (str): The key of the player in the players_dict.
            players_dict (dict): A dictionary containing the players' letter tiles.

        Returns:
            dict: The updated players_dict with the 'Ö' tile replaced by the specified letter.
        """
        # Remove the 'Ö' tile from the player's list of tiles
        players_dict[player_turn][0].remove('Ö')
        
        # Add the specified letter to the player's list of tiles
        players_dict[player_turn][0].append(ö)
        
        # Return the updated dictionary of players' letter tiles
        return players_dict

    

    def add_already_placed_letter(self, word, direction, pos, scrabbleboard):
        """
        Given a word, its direction, a starting position, and the current Scrabble board, 
        this function returns a list of letters that have already been placed on the board
        in the same row or column as the word.
        
        Args:
            word (str): The word being played.
            direction (str): The direction of the word, either 'H' (horizontal) or 'V' (vertical).
            pos (tuple): A tuple representing the starting position of the word on the board.
            scrabbleboard (list): A 2D list representing the current Scrabble board.
        
        Returns:
            list: A list of letters that have already been placed on the board in the same row
            or column as the word.
        """
        letters_to_apply = []
        
        # Check if there is already a letter at the starting position
        if scrabbleboard[pos[0]][pos[1]] in ALPHABET:
            letters_to_apply.append(scrabbleboard[pos[0]][pos[1]])
        
        # Determine the row and column of the next letter based on the direction
        row, col = pos
        if direction == 'H':
            col += 1
        elif direction == 'V':
            row += 1
        
        # Check for letters in the same row or column as the word
        for letter in word:
            if scrabbleboard[row][col] in ALPHABET:
                letters_to_apply.append(scrabbleboard[row][col])
            if direction == 'H':
                col += 1
            elif direction == 'V':
                row += 1
        
        return letters_to_apply


    def contains_letters_on_hand(self, word, player_turn, players_dict, direction, pos, scrabbleboard):
        """Checks if a player has the necessary letters in their hand to play a word on the board.

        Args:
            word (str): The word being placed on the board.
            player_turn (int): The player making the move.
            players_dict (dict): A dictionary containing information about each player.
            direction (str): The direction in which the word is being placed ("across" or "down").
            pos (tuple): The starting position of the word on the board.
            scrabbleboard (list): The current state of the Scrabble board.

        Returns:
            bool: True if the player has the necessary letters in their hand, False otherwise.
        """
        # Get the letters that will overlap with the current word
        overlapping_letters = self.add_already_placed_letter(word, direction, pos, scrabbleboard)

        # Make a copy of the player's current hand and add the overlapping letters to it
        store_hand = players_dict[player_turn][0].copy()
        store_hand += overlapping_letters

        # Check if the player has all the letters needed to play the word
        for letter in word.upper():
            if letter not in store_hand:
                return False
            store_hand.remove(letter)

        return True


    

    
    def valid_words_touching(self, word, direction, pos, scrabbleboard):
        """Checks if all the perpendicular words formed by the given word on the board are valid.

        Args:
            word (str): The word being placed on the board.
            direction (str): The direction in which the word is being placed ("across" or "down").
            pos (tuple): The starting position of the word on the board.
            scrabbleboard (list): The current state of the Scrabble board.

        Returns:
            bool: True if all the perpendicular words are valid, False otherwise.
        """
        # Get a list of all the perpendicular words formed by the given word on the board
        perpendicular_tuple = self.get_perpendicular_word_list(word, direction, pos, scrabbleboard)

        # Check if all the perpendicular words are valid (i.e. exist in the dictionary)
        # Ignore any perpendicular words that could not be formed (i.e. None values)
        return all([self.scrabble_word_logic.is_word_valid(perpen_tuple[0]) for perpen_tuple in perpendicular_tuple if perpen_tuple is not None])



    def get_perpendicular_word_list(self, word: str, direction: str, pos: tuple[int, int], scrabbleboard: list[list[str]]) -> list[tuple[str, tuple[int, int]]]:
        """
        Returns a list of perpendicular words that can be formed by the given `word` on the Scrabble board, given its
        `direction` and starting `pos`. 

        Args:
            word (str): The word to be played.
            direction (str): The direction in which the word is being played: 'H' for horizontal or 'V' for vertical.
            pos (tuple): A tuple representing the starting position of the word on the Scrabble board as (row, column).
            scrabbleboard (list): A list of lists representing the current state of the Scrabble board.

        Returns:
            list: A list of tuples, where each tuple contains a perpendicular word that can be formed by the given `word`,
            as well as the starting position of that word. Each tuple is of the form `(perpendicular_word, start_pos)`.
        """
        # Define a lambda function to change the position based on the direction
        if direction == 'V':
            change_pos = lambda i: (pos[0]+1*i, pos[1])
        else:
            change_pos = lambda i: (pos[0], pos[1]+1*i)

        # Get a list of perpendicular words formed by the input word and returns it
        return [self.get_word_in_direction_with_start_pos(letter, direction, change_pos(i), scrabbleboard) for i, letter in enumerate(word)]
        

    def get_word_in_direction_with_start_pos(self, letter, direction, pos, scrabbleboard):
        """
        Finds the longest word that can be formed in the given `direction` starting from the given `pos` on the `scrabbleboard`
        with the given `letter` added to it.

        Args:
            letter (str): The letter to be added to the word.
            direction (str): The direction in which to look for the word: either 'H' for horizontal or 'V' for vertical.
            pos (tuple): A tuple representing the starting position of the word on the Scrabble board as (row, column).
            scrabbleboard (list): A list of lists representing the current state of the Scrabble board.

        Returns:
            tuple: A tuple containing the longest word that can be formed in the given `direction` starting from the given `pos` on the `scrabbleboard`
            with the given `letter` added to it, and the starting position of the word on the board. Returns None if no word can be formed.

        """
        # Determine the two halves of the word in the given direction
        first_half, second_half = ((-1,0), (1, 0)) if direction == 'H' else ((0,-1), (0, 1))
        
        # Get the letters before and after the current position in the given direction
        before = self.get_letters_beside(pos, scrabbleboard, first_half)
        start_pos = (pos[0]-len(before), pos[1]) if direction == 'H' else (pos[0], pos[1]-len(before))
        after = self.get_letters_beside(pos, scrabbleboard, second_half)
        
        # If there are letters before or after the current position, a word can be formed
        if before or after:   
            return (before[::-1] + letter + after, start_pos)

        

    def get_letters_beside(self, pos, scrabbleboard, half):
        """
        Returns a string of letters that are beside the given position on the Scrabble board in the specified direction.

        Args:
            pos (tuple): The position of the starting letter as a (row, column) tuple.
            scrabbleboard (list): The current state of the Scrabble board represented as a list of lists.
            half (tuple): The direction in which to search for letters. Either (-1, 0), (1, 0), (0, -1), or (0, 1).

        Returns:
            str: A string of letters that are beside the starting position on the board in the given direction.
        """
        # Initialize the row and column indices for the starting position plus the given direction.
        row, col = pos[0] + half[0], pos[1] + half[1]
        # Initialize an empty string to store the adjacent letters.
        word_string = ''
        # Loop through the board in the given direction, adding adjacent letters to the word string.
        while 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and scrabbleboard[row][col] in ALPHABET:
            word_string += scrabbleboard[row][col]
            # Update the row and column indices to check the next letter in the given direction.
            row, col = row + half[0], col + half[1]
        # Return the resulting string of adjacent letters.
        return word_string



    def use_of_your_letters(self, word, direction, pos, scrabbleboard):
        """
        Determines which letters of `word` can be played on Scrabble board starting from `pos` in `direction`.
        Returns a boolean list indicating if each letter can be played.

        Args:
            word (str): The input word to play.
            direction (str): 'H' for horizontal or 'V' for vertical play.
            pos (tuple): Starting position on board as (row, column).
            scrabbleboard (list): Current state of the Scrabble board.

        Returns:
            list: Boolean list of same length as `word`. True if letter can be played, False otherwise.
        """
        # Initialize an empty list to hold the results.
        your_letters_list = []
        
        # Iterate through each letter in the input word.
        for letter in word:
            # Check if the current board position is empty or already has a letter.
            if scrabbleboard[pos[0]][pos[1]] in ALPHABET:
                # If the position already has a letter, the current input letter cannot be played.
                your_letters_list.append(False)
            else:
                # If the position is empty, the current input letter can be played.
                your_letters_list.append(True)
            
            # Move to the next board position based on the chosen direction.
            if direction == 'H':
                # For horizontal play, increment the column position.
                pos = (pos[0], pos[1]+1)
            elif direction == 'V':
                # For vertical play, increment the row position.
                pos = (pos[0]+1, pos[1])
        
        # Return the final result list.
        return your_letters_list


class LegalSwap:
    def __init__(self) -> None:
        pass

    def legal_continue_input(self, continue_input):
        """Check if the continue_input is a legal input.
        
        Args:
        continue_input (str): A string containing the player's input for whether they want to continue playing or not. Must be either 'Y' for yes or 'N' for no.
        
        Returns:
        bool: True if continue_input is a legal input ('Y' or 'N'), False otherwise.
        """
        return continue_input in ['Y', 'N']


    def legal_to_swap(self, player_turn, players_dict, letter):
        """Check if the letter is legal to swap for the current player.
        
        Args:
        player_turn (int): An integer indicating the current player's turn.
        players_dict (dict): A dictionary containing information about the players and their current letters.
        letter (str): A string representing the letter the player wants to swap.
        
        Returns:
        bool: True if the letter is in the player's current set of letters, False otherwise.
        """
        return letter in players_dict[player_turn][0]

    
class LegalDirection:
    def __init__(self):
        pass

    def legal_direction(self, direction):
        """
        Checks if the given direction is a valid direction or not.

        Args:
            direction (str): A string representing the direction of the word placement.

        Returns:
            bool: True if the direction is 'V' or 'H', False otherwise.
        """
        return direction in ['V', 'H']
