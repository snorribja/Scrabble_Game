import csv
import random


class ScrabbleBag:
    def __init__(self):
        """Initializes the Scrabble letter bag with letter values and frequencies loaded from a CSV file."""
        self.letter_bag = []  # Initialize an empty list to hold the letters in the bag
        self.letter_values = {}  # Initialize an empty dictionary to hold the point values of each letter
        self.letter_frequencies = {}  # Initialize an empty dictionary to hold the frequency of each letter
        filename = 'files/scrabble_letters_value_frequency.csv'  # Specify the filename of the CSV file to read

        # Open the CSV file and loop through each row
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                letter, value, frequency = row  # Extract the letter, value, and frequency from the current row
                self.letter_values[letter] = int(value)  # Add the letter's point value to the letter_values dictionary
                self.letter_frequencies[letter] = int(frequency)  # Add the letter's frequency to the letter_frequencies dictionary
                for _ in range(int(frequency)):
                    # Add the correct number of instances of the letter to the letter_bag list
                    self.letter_bag.append(letter)


    def draw_tiles(self, unused_tiles=None, num_tiles=7):
        """Draws a specified number of tiles from the letter bag.

        Args:
            unused_tiles (list, optional): A list of tiles to return to the letter bag. Defaults to None.
            num_tiles (int, optional): The number of tiles to draw. Defaults to 7.

        Returns:
            list: A list of the drawn tiles.
        """
        # Return any unused tiles to the letter bag
        if unused_tiles:
            for tile in unused_tiles:
                self.letter_bag.append(tile)

        # If we need more tiles than are available in the letter bag, draw the maximum number of tiles
        if num_tiles > len(self.letter_bag):
            num_tiles = len(self.letter_bag)

        # Draw the requested number of tiles at random from the letter bag
        tiles = random.sample(self.letter_bag, num_tiles)

        # Remove the drawn tiles from the letter bag
        for tile in tiles:
            self.letter_bag.remove(tile)

        # Return the drawn tiles
        return tiles


    def tiles_left_in_bag(self):
        """Returns the number of tiles remaining in the letter bag.

        Returns:
            int: The number of tiles remaining in the letter bag.
        """
        return len(self.letter_bag)


    def get_tile_value(self, tile):
        """Returns the point value of a given tile.

        Args:
            tile (str): The tile to check.

        Returns:
            int: The point value of the tile.
        """
        return self.letter_values[tile]


    def __str__(self):
        """Returns a string representation of the letter bag.

        Returns:
            str: A string representation of the letter bag.
        """
        return str(self.letter_bag)
