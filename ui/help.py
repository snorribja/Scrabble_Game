

class Help:
    def __init__(self):
        pass

    def with_commands(self):
        self.rules()  
        self.ö_letter()   
        input("Enter any command to return: ")
        
    def rules(self):
        print('The rules are: ')
        rules = 'At the beginning of the game, each player draws seven letter tiles from a bag of 100 tiles. \nThe players take turns forming words on the game board using their own tiles and tiles already on the board. \nThe first player must place a word on the center square of the board, which is marked with a star. \nWords can be placed either vertically or horizontally and must connect with at least one existing tile on the board. \nPlayers can score points by placing tiles on squares with bonus values, such as double letter score, triple letter score, double word score, and triple word score. \nEach tile has a point value, and the player scores the total value of their word by adding up the point values of each tile in the word. \nIf a player uses all seven of their tiles in one turn, they receive a bonus of 50 points. \nIf a player is unable to form a word, they can choose to swap out one or more of their tiles for new ones from the bag. \nThe game ends when all tiles have been drawn from the bag and one player has used all of their tiles or no player can form any more words. \nThe player with the highest score at the end of the game wins.'
        for i,j in enumerate(rules.split('\n'), start=1):
            print(i,'.', j)

    def ö_letter(self):
        print('\nThe letter Ö works as a blank tile and has the value 0\n')