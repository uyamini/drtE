from src import Column
import numpy as np
from itertools import starmap

ENABLED_STR_COLS = True

def _array_args():
    arrays = [np.array(['0.0', '1', '1.0', '-1.0']),
              np.array(['1', '2', '3', '4', '5', 'nan']),
              np.array([' ', 'na', '2', 'string', '1', '-100', 'more string'])]
    return [ (arrays[i], 0) for i in range(len(arrays)) ]

def test_median():
    cols = starmap(Column, _array_args())
    true_medians = [0.5, 3, 1]
    medians = list(map(lambda c: c.quantile(0.5), cols))
    assert np.allclose(true_medians, medians)

def test_mode():
    # the arrays I've been using aren't great for this problem but
    # I don't want to change them bc then I'd have to change all
    # the other test cases
    cols = [Column(np.array(['0', '2', '-1', '2', '0', '2']), 0),
            Column(np.array(['1', 'na', ' ', '1', '2', 'string']), 0),
            Column(np.array(['-1', '-100', '1lbs', '-100']), 0)]
    true_modes = ['2', '1', '-100']
    for i in range(len(true_modes)):
        assert cols[i].mode == true_modes[i]

def test_col_type():
    cols = starmap(Column, _array_args())
    true_types = ['float', 'int', 'alpha']
    types = list(map(lambda c: c.column_type, cols))
    for i in range(len(types)):
        assert true_types[i] == types[i], f'{true_types} != {types}'
    assert Column(np.array(['string']), 0).column_type == 'alpha'
    col2 = Column(np.array(['not email', 'michael@gmail.com', 'michael@u.northwestern.edu']), 0)
    assert col2.column_type == 'email'

def test_quants():
    cols = starmap(Column, _array_args())
    true_quants = np.array([[-1, -0.25, 0.5, 1, 1],
                            [1, 2, 3, 4, 5],
                            [-100, -49.5, 1, 1.5, 2]])
    quants = list(map(lambda c: c._quants, cols))
    assert np.allclose(true_quants, quants)

def test_str_cols():
    if ENABLED_STR_COLS:
        cols = starmap(Column, _array_args())
        true_strs = [[], [], [' ', 'na', 'string', 'more string']]
        strs = list(map(lambda c: c.str_els, cols))
        for i in range(len(strs)):
            assert np.all(np.array(true_strs[i], dtype = str) == strs[i]), f'{true_strs} != {strs}'
        
def test_by_count():
    cols = starmap(Column, _array_args())
    for c in cols:
        for el in c.by_count:
            assert c.by_count[el] == 1

    dup_col = Column(np.array(['1', '2', '3', '3', '2', '1']), 0)
    for el in dup_col.by_count:
        assert dup_col.by_count[el] == 2
