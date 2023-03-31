from data.scrabble_word_data import *


class ScrabbleWordLogic:
    def __init__(self):
        self.data = ScrabbleWordData()

    def is_word_valid(self, word: str):
        word_set = self.data.get_words()
        return word.upper() in word_set

    def add_word(self, word):
        if not self.is_word_valid(word):
            self.data.add_word(word)

    def make_word_with_ö(self, word, ö):
        ö_index = word.index('Ö')
        if ö_index == 0:
            return ö + word[1:].upper()
        elif ö_index == len(word):
            return word[:-1].upper() + ö
        else:
            return word[:ö_index].upper()+ ö + word[1+ö_index:].upper() 
        