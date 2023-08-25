import numpy as np
from .rule_base import RuleBaseClass
import en_core_web_sm
nlp = en_core_web_sm.load()

COUNT_PER_100_LINES = 2
_MIN_CATS = 2
_MAX_CATS = 5

class WrongCategory (RuleBaseClass):
    """Checks if a cell is different from the most common categories."""
    def __init__(self):
        #Cookies and Cream
        self.color = (232, 215, 173)
        self.name = 'Category Mismatch'
        
    def is_dirty(self, cell_str, col):
        if col.column_type != 'alpha': return False
        counts = col.by_count[cell_str]
        cats = col.strs_over_thresh.shape[0]
        if col.length > 100:
            per_100 = lambda n: 100 * n / col.length 
            counts = per_100(counts)
            cats = per_100(cats)

        return (counts <= COUNT_PER_100_LINES and 
                cats >= _MIN_CATS and
                cats <= _MAX_CATS)

    def message(self, cell_str, col):
        return ('This row appears to have a small number of categories, but ' +
                f'{cell_str} is not one of them.')

    def clean(self, inds, sheet, col, all_dirty):
        cur_tok = nlp(str(sheet[tuple(inds)]))
        tokens = nlp(' '.join(col.strs_over_thresh))

        return max(tokens, key = lambda t: cur_tok.similarity(t)).text
