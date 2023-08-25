from Levenshtein import distance
from .num_outliers import _num_is_outlier
from ..utilities import can_be_float

_QUANT_SCALE = 1.5

def str_outlier(cell_str, col):
    """Takes the string version of the cell and returns whether it is inconsistent with other cells.

    Also returns False if the string can be cast as a float

    Args:
        cell_str (str) : the raw text of that cell
        col (Column) : container for generic info about the column of that cell

    Returns:
        is_outlier (bool) : whether that cell is an outlier linguistically
    """
    if can_be_float(cell_str): return False
    total = 0
    for row in col.str_els:
        total += distance(cell_str, row)
    return _num_is_outlier(total / col.str_els.shape[0], 
                           col.lev_quants[1], 
                           col.lev_quants[3],
                           _QUANT_SCALE)
                           