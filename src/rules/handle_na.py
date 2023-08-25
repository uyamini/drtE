from .rule_base import RuleBaseClass

class IsNA (RuleBaseClass):
    """Checks is cells are 'na'."""
    def __init__(self):
        self.nas = {"n/a", "na", "--", "-", "nan", "NaN", "not applicable"}
        #Crayola's Periwinkle
        self.color = (199, 206, 234)
        self.name = 'NA'

    def is_dirty(self, cell_str, col):
        if cell_str.lower() in self.nas and cell_str != 'NA': 
            return True
        else:
            return False

    def message(self, cell_str, col):
        return (f'This cell "{cell_str}" was interpreted as a variation of "NA". ' +
                'We suggest standardizing all such cells to "NA".')

    def clean(self, inds, sheet, col, all_dirty):
        return 'NA'
