from ..utilities import can_be_float, can_be_int
from .rule_base import RuleBaseClass

class IsIncorrectDataType (RuleBaseClass):
    """Checks if cells are the wrong datatype."""
    def __init__(self):
        self.num_chars = {'-', '.'} | { str(i) for i in range(10) }
        #Columbia Blue 
        self.color = (192, 228, 241)
        self.name = 'Datatype Inconsistency'

    def is_dirty(self, cell_str, col):
        if cell_str == '': return False
        if can_be_int(cell_str):
            return col.column_type != 'int' and col.column_type != 'float'
        if can_be_float(cell_str):
            return col.column_type != 'float'
        return col.column_type != 'alpha'

    def message(self, cell_str, col):
        interp_type = 'alphabetical'
        if can_be_int(cell_str):
            interp_type = 'an integer'
        elif can_be_float(cell_str):
            interp_type = 'a decimal number'
        true_type = 'alphabetical words'
        if col.column_type == 'int':
            true_type = 'integers'
        elif col.column_type == 'float':
            true_type = 'decimal numbers'
        return (f'The cell {cell_str} was interpreted as {interp_type}, in contrast ' +
                f"to the column's most common datatype, {true_type}.")

    def clean(self, inds, sheet, col, all_dirty):
        if (col.column_type == 'int' or 
            col.column_type == 'float'):
            tup_inds = tuple(inds)
            splits = []
            word = ''
            is_num = sheet[tup_inds][0] in self.num_chars
            for c in sheet[tup_inds]:
                c_num = c in self.num_chars
                if c_num == is_num:
                    word += c
                else:
                    splits.append(word)
                    word = c
                    is_num = c_num
            for w in splits:
                if can_be_float(w):
                    return w

        return col.generic_clean(inds, sheet, all_dirty)
