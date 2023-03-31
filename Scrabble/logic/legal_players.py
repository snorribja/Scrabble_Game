
class LegalPlayers:
    def __init__(self) -> None:
        pass

    def legal_players_num(self, players_num):
        """
        Check if the input number of players is valid.

        Args:
        players_num (str): A string representing the number of players in the game.

        Returns:
        bool: True if the input is a valid number of players (between 2 and 4 inclusive), and False otherwise.
        """
        # Check if the input is a numeric string
        if players_num.isnumeric():
            # Check if the numeric value is between 2 and 4
            return int(players_num) < 5 and int(players_num) > 1
        else:
            return False

