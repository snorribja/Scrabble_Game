from logic.scrabble_bag import ScrabbleBag


class GameRunning():
    def __init__(self):
        self.scrabble_bag = ScrabbleBag()
    
    def game_running(self, players_dict, pass_turn_counter):
        """
        Check if the game is still running or has ended.

        Args:
        players_dict (dict): A dictionary containing information about the players and their tiles.
        pass_turn_counter (int): The number of passes made by players.

        Returns:
        bool: Returns True if the game is still running, otherwise False.
        """
        num_players = len(players_dict.keys())*2
        for player in players_dict.keys():
            if players_dict[player][0] == []:
                return False
        return pass_turn_counter < num_players

    

    def calculate_points(self, players_dict):
        """
        Calculates the points for each player and the bonus point for the player who finishes first.

        Args:
        players_dict (dict): A dictionary containing information about the players and their tiles.

        Returns:
        dict: A dictionary containing information about the players, their tiles and points.
        """
        bonus_point = 0
        finish_player = str()
        for name in players_dict.keys():
            if players_dict[name][0] == []:
                finish_player = name
            point = 0
            for letter in players_dict[name][0]:
                point += self.scrabble_bag.get_tile_value(letter)
                bonus_point += point
                players_dict[name][1] -= point
        if finish_player != '':
            players_dict[finish_player][1] += bonus_point
        return players_dict

    
    def find_winner(self, players_dict):
        """
        Finds the winner of the game.

        Args:
        players_dict (dict): A dictionary containing information about the players and their tiles.

        Returns:
        str: The name of the winner.
        """
        highest_points = -float('infinity')
        winner = str()
        for player in players_dict.keys():
            if players_dict[player][1] == highest_points:
                winner += ' and ' + player
            if players_dict[player][1] > highest_points:
                highest_points = players_dict[player][1]
                winner = player
        return winner


    def end_of_game(self, players_dict):
        """
        Calculates the points for each player, finds the winner and returns the points and name of the winner.

        Args:
        players_dict (dict): A dictionary containing information about the players and their tiles.

        Returns:
        tuple: A tuple containing the points and name of the winner.
        """
        players_dict = self.calculate_points(players_dict)
        winner = self.find_winner(players_dict)
        return players_dict[winner][1], winner[0].upper() + winner[1:].lower()
