from logic.scrabbleboard import *
from logic.play_turn import *
from logic.scrabble_word_logic import ScrabbleWordLogic
from logic.legal_pos_and_dir import *
from logic.legal_players import LegalPlayers
from ui.scrabble_word_ui import *
from ui.hand_ui import *
from logic.game_running import GameRunning
from pyfiglet import Figlet
import os

class Play_Scrabble(Scrabbleboard):
    def __init__(self):
        super().__init__()
        self.scrabble_word_logic = ScrabbleWordLogic()
        self.legal_pos_logic = LegalPosition()
        self.legal_dir_logic = LegalDirection()
        self.legal_players = LegalPlayers()
        self.hand_ui = HandUI()
        self.legal_swap = LegalSwap()
        self.player_names = list()
        self.player_turn = None
        self.pass_turn_counter = 0
        self.first_placement = True
        self.game_is_running = GameRunning()
        self.custom_fig = Figlet(font='graffiti')


    def game_of_scrabble(self):
        self.get_players()
        os.system('clear')
        self.the_game()


    def get_players(self):
        """
        Asks for the number of players and their names, and initializes their tiles and scores.
        """
        while True:
            number_of_players = input("How many players are there: ")
            if self.legal_players.legal_players_num(number_of_players): # Check if the number of players is legal
                counter = 1
                while counter <= int(number_of_players):
                    name = input(f'Enter name for player {counter}: ')
                    if name in self.players_dict.keys() or name == '': # Check if the name is already taken or blank
                        print('Name already taken or blank! Try again')
                    else:
                        uppercase_name = name[0].upper() + name[1:] # Capitalize the first letter of the name
                        self.players_dict[uppercase_name] = [self.scrabble_bag.draw_tiles(), 0] # Initialize the player's tiles and score
                        counter += 1
                self.player_names = list(self.players_dict.keys()) # Create a list of the player names
                self.player_turn = self.player_names[0] # Set the first player as the current turn
                break
            else:
                print('Illegal amount of players!')

    def the_game(self):
        while self.game_is_running.game_running(self.players_dict, self.pass_turn_counter):
            print(self)
            print(self.hand_ui.the_hand(self.player_turn, self.players_dict))
            choice = self.get_choice()
            if choice == '1':
                self.place_choice()
            elif choice == '2':
                self.swapping_letters()
            elif choice == '3':
                self.pass_turn()
            elif choice == '4':
                pass
            self.change_turn()
        winners_points, winner = self.game_is_running.end_of_game(self.players_dict)
        
        print(colored(self.custom_fig.renderText(f'{winner} won with {winners_points} points!'), color='yellow', attrs=['blink', 'bold']))


    def swapping_letters(self):
        letter_to_swap = self.get_letter_wanting_to_swap()
        self.swap_letters(letter_to_swap)


    def get_letter_wanting_to_swap(self):
        """Prompts the player to enter letters they want to swap and returns a list of those letters.

        Returns:
            list: A list containing the letters the player wants to swap.

        """
        swap_letters = list()
        getting_letters = True

        # Continue asking the player for letters to swap until they don't want to swap any more.
        while getting_letters:
            letter = input('Enter a letter you want to swap: ').upper()

            # If the letter is in the player's hand, add it to the list of letters to swap.
            if self.legal_swap.legal_to_swap(self.player_turn, self.players_dict, letter):
                swap_letters.append(letter)
            else:
                print("You don't have this letter in your hand!")

            # Ask the player if they want to enter another letter to swap.
            continue_input = input('Do you want to enter another one (Y/N)? ').upper()

            # If the player wants to continue, keep getting letters to swap.
            if self.legal_swap.legal_continue_input(continue_input):
                if continue_input == "N":
                    getting_letters = False
            else:
                print('Type either "Y" or "N": ')

        return swap_letters


    def place_choice(self):
        """
        Handles the player's choice of where to place their word on the board. 
        If the placement is allowed, the word is placed and points are added 
        to the player's score. Otherwise, an error message is displayed.
        """
        try:
            word, direction, start_pos = self.get_word()
            letters_to_apply = self.legal_pos_logic.add_already_placed_letter(word, direction, start_pos, self.scrabbleboard)
            self.players_dict[self.player_turn][0] += letters_to_apply
            if self.allow_to_place(word, direction, start_pos):
                self.add_to_hand(word, direction, start_pos)
                self.place_word(word, direction, start_pos)
                self.first_placement = False
            else:
                self.players_dict[self.player_turn][0] -= letters_to_apply
                print("Not allowed to place this word there!")
        except TypeError:
            pass

    def get_choice(self):
        """
        Prompts the current player to choose between three actions: place a word on the table, swap letters, or pass the turn.

        Returns:
        - command (str): the player's choice of action, which can be '1' for placing a word, '2' for swapping letters, or '3' for passing the turn.
        """
        # Prompt the current player and display the available choices
        print(f"{self.player_turn[0].upper()}{self.player_turn[1:]}'s turn")
        while True:
            print("Choices: 1. Place word on table\n \t 2. Swap letters\n \t 3. Pass turn")
            # Get the player's input and check if it is a valid choice
            command = input("Enter your choice: ")
            if command in ['1', '2', '3']:
                return command
            # If the input is not valid, prompt the player to try again
            print("Invalid choice! Try again.")


    def get_word(self):
        while True:
            start_pos = input('Enter starting position: ')
            if not (self.legal_pos_logic.valid_starting_pos(start_pos) and self.legal_pos_logic.is_on_board(start_pos)):
            
                print('This position is not on board! Try again')
                continue

            start_pos = self.legal_pos_logic.get_position(start_pos)
            direction = input('Do you want to place the word (V)ertically or (H)orizontally: ').upper()
            if not self.legal_dir_logic.legal_direction(direction):
                print('Not a valid direction! Try again')
                continue

            word = input('Enter word: ').upper()
            if 'Ö' in word:
                ö = self.get_ö().upper()
                word = self.scrabble_word_logic.make_word_with_ö(word, ö)
                self.players_dict = self.legal_pos_logic.replace_ö(ö, self.player_turn, self.players_dict) 

            if self.scrabble_word_logic.is_word_valid(word):
                if self.legal_pos_logic.contains_letters_on_hand(word, self.player_turn, self.players_dict, direction, start_pos, self.scrabbleboard):
                    return word, direction, start_pos
                else:
                    print("You don't contain letters for this word!")

            else: 
                print("This word is not in the Scrabble dictionary!!")
                break


    def get_ö(self):
        """
        This function gets the letter for Ö from the user and returns it.

        Inputs:
        - None

        Outputs:
        - ö: string, the letter for Ö
        """
        while True:
            # Get the input for Ö from the user and convert it to uppercase
            ö = input('What is the letter for Ö: ').upper()

            # Check if the entered Ö is valid
            if ö in ALPHABET:
                return ö
            else:
                # Print a message saying the entered Ö is not valid and repeat the loop
                print('Not a valid Ö!')

            