import pandas as pd
import numpy as np
from src.utilities import can_be_float, float_is_int
from .rule_base import RuleBaseClass

_QUANT_SCALE = 1.5

def _num_is_outlier(x, perc25, perc75, quant_scale = _QUANT_SCALE):
    """Takes a number and returns if it's an outlier."""
    iqr = perc75 - perc25
    return (x < perc25 - quant_scale * iqr or
            x > perc75 + quant_scale * iqr)

class NumOutlier (RuleBaseClass):
    """Checks if cells are numeric outliers."""
    def __init__(self):
        #Dirty White
        self.color = (226, 240, 203)
        self.name = 'Outliers'

    def is_dirty(self, cell_str, col):
        if not can_be_float(cell_str): return False
        return _num_is_outlier(float(cell_str), col.quantile(0.25), col.quantile(0.75))

    def message(self, cell_str, col):
        med = col.quantile(0.5)
        above = 'above' if float(cell_str) > med else 'below'
        return f'This cell was way {above} the median, which was {med}.'

    def clean(self, inds, sheet, col, all_dirty):
        f = float(sheet[tuple(inds)])
        if not self.is_dirty(str(f * 10), col):
            if float_is_int(f * 10):
                return str(round(f * 10))
            return str(f * 10)

        with_dec = f'0.{f}'
        if can_be_float(with_dec) and not self.is_dirty(with_dec, col):
            return with_dec
            
        q = col.quantile(0.5)
        if float_is_int(q) or col.column_type == 'int':
            return str(round(q))
        return str(q)
