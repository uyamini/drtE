class RuleBaseClass:
    """An abstract base class for all predicates.
    
    Args:
        None
    """
    def __init__(self):
        self.color = (-1, -1, -1)
        self.name = ''
        raise NotImplementedError

    def is_dirty(self, cell_str, col):
        """Returns whether the string is dirty.
        
        Args:
            cell_str (str) : the string to check
            col (Column) : container class with information about cell_str's column

        Returns:
            dirty (bool) : whether or not the cell is dirty
        """
        raise NotImplementedError

    def message(self, cell_str, col):
        """Generates a user-readable message explaining why the cell is dirty.
        
        Args:
            cell_str (str) : the dirty string
            col (Column) : container class with information about cell_str's column

        Returns:
            why (str) : why the string is dirty
        """
        raise NotImplementedError

    def clean(self, inds, sheet, col, all_dirty):
        """Returns what to put in the dirty cell based on col.
        
        Args:
            inds (np.array) : a [y, x] pair indicating which cell to clean
            sheet (np.array) : a 2D matrix of strings
            col (Column) : information about the dirty cell's column
            all_dirty (np.array) : an array of all [y, x] pairs that are dirty

        Returns:
            prediction (str) : what the rule predicts should go there
        """
        return col.generic_clean(inds, sheet, all_dirty)
        
    def __eq__(self, other):
        """Returns whether the two rules are the same type."""
        return type(self) == type(other)

    def __hash__(self):
        """Allows for using RuleBase objects as keys in a dictionary."""
        return hash(type(self))