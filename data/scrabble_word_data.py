class ScrabbleWordData:
    def __init__(self):
        self.filename = 'files/legal_scrabble_words.txt'

    def add_word(self, word):
        """
        Adds a word to the word list file.

        Args:
            word (str): The word to be added to the file.

        """
        with open(self.filename, 'a') as f:
            f.write(word.upper() + '\n')

            
    def get_words(self):
        """
        Retrieves all words in the word list file.

        Returns:
            word_set (set): A set of all words in the word list file.
        """
        word_set = set()
        with open(self.filename, 'r') as f:
            for line in f:
                word = line.strip()
                word_set.add(word)
        return word_set
