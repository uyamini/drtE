import numpy as np
from spellchecker import SpellChecker
from .rule_base import RuleBaseClass

class HasTypo (RuleBaseClass):
    """Checks if a cell has a typo in it."""
    def __init__(self):
        self.checker = SpellChecker()
        #Phillipine Silver 
        self.color = (177, 177, 177)
        self.name = 'Typos'

    def _typo_word(self, s):
        """Returns whether s is likely to be a typo."""
        w = ''.join(filter(lambda c: c.isalnum(), s))
        if len(w) < 4:
            return False
        return self._clean_word(w).lower() != w.lower()

    def _clean_word(self, s):
        """Returns the most likely word the user meant based on s."""
        if s == '': return s
        return self.checker.correction(s)

    def is_dirty(self, cell_str, col):
        words = cell_str.split(' ')
        return any(map(self._typo_word, words))

    def message(self, cell_str, col):
        words = cell_str.split(' ')
        for word in words:
            if self._typo_word(word):
                return f'{word} appears to be a typo. Did you mean {self._clean_word(word)}?'
        raise ValueError(f'No typo present in {cell_str}.')

    def clean(self, inds, sheet, col, all_dirty):
        words = sheet[tuple(inds)].split(' ')
        for i in range(len(words)):
            if self._typo_word(words[i]):
                words[i] = self._clean_word(words[i])
        return ' '.join(words)
