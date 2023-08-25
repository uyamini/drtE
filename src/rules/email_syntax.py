import re
from .rule_base import RuleBaseClass

#Code from : https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
class EmailChecker (RuleBaseClass):
    """Checks if a cell is an email when it should/shouldn't be."""
    def __init__(self):
        self.regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        #Tea Green
        self.color = (208, 246, 210)
        self.name = 'Email Inconsistency'

    def _is_email(self, cell_str):
        """Returns whether cell_str is an email."""
        return re.fullmatch(self.regex, cell_str) is not None

    def is_dirty(self, cell_str, col):
        if col.column_type == 'email':
            return not self._is_email(cell_str)
        return self._is_email(cell_str)

    def message(self, cell_str, col):
        if self._is_email(cell_str):
            return f'{cell_str} was interpreted as an email, which is not consistent with the rest of the column.'
        return f'The column mostly has emails, but {cell_str} was not interpreted as one.'
